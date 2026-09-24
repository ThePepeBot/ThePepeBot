//! pepebot-distributor
//!
//! DRAFT — NOT AUDITED — NOT DEPLOYED — NOT BUILT IN CI.
//! A sketch of the pull-based distributor described in contracts/README.md.
//! It exists so the design can be reviewed in code. Do not deploy it.

use anchor_lang::prelude::*;
use anchor_lang::solana_program::keccak;
use anchor_spl::token_interface::{self, Mint, TokenAccount, TokenInterface, TransferChecked};

declare_id!("11111111111111111111111111111111"); // placeholder

#[program]
pub mod pepebot_distributor {
    use super::*;

    /// Multisig posts a root for an epoch. The vault must already hold `total`.
    pub fn post_epoch(ctx: Context<PostEpoch>, epoch: u64, root: [u8; 32], total: u64, claim_until: i64) -> Result<()> {
        require!(ctx.accounts.vault.amount >= total, DistError::Underfunded);
        let e = &mut ctx.accounts.epoch;
        e.authority = ctx.accounts.authority.key();
        e.mint = ctx.accounts.mint.key();
        e.epoch = epoch;
        e.root = root;
        e.total = total;
        e.claimed = 0;
        e.claim_until = claim_until;
        e.bump = ctx.bumps.epoch;
        Ok(())
    }

    /// Holder claims their leaf. A receipt PDA per (epoch, holder) makes this one-shot.
    pub fn claim(ctx: Context<Claim>, amount: u64, proof: Vec<[u8; 32]>) -> Result<()> {
        let e = &mut ctx.accounts.epoch;
        require!(Clock::get()?.unix_timestamp <= e.claim_until, DistError::Expired);

        let leaf = keccak::hashv(&[
            &e.epoch.to_le_bytes(),
            ctx.accounts.holder.key().as_ref(),
            e.mint.as_ref(),
            &amount.to_le_bytes(),
        ]).0;
        require!(verify(&proof, e.root, leaf), DistError::BadProof);

        e.claimed = e.claimed.checked_add(amount).ok_or(DistError::Overflow)?;
        require!(e.claimed <= e.total, DistError::Overflow);

        let epoch_bytes = e.epoch.to_le_bytes();
        let seeds: &[&[u8]] = &[b"epoch", e.mint.as_ref(), &epoch_bytes, &[e.bump]];
        token_interface::transfer_checked(
            CpiContext::new_with_signer(
                ctx.accounts.token_program.to_account_info(),
                TransferChecked {
                    from: ctx.accounts.vault.to_account_info(),
                    mint: ctx.accounts.mint.to_account_info(),
                    to: ctx.accounts.holder_ata.to_account_info(),
                    authority: e.to_account_info(),
                },
                &[seeds],
            ),
            amount,
            ctx.accounts.mint.decimals,
        )?;
        ctx.accounts.receipt.bump = ctx.bumps.receipt;
        Ok(())
    }
}

fn verify(proof: &[[u8; 32]], root: [u8; 32], leaf: [u8; 32]) -> bool {
    let mut h = leaf;
    for p in proof {
        h = if h <= *p { keccak::hashv(&[&h, p]).0 } else { keccak::hashv(&[p, &h]).0 };
    }
    h == root
}

#[account]
#[derive(InitSpace)]
pub struct Epoch {
    pub authority: Pubkey,
    pub mint: Pubkey,
    pub epoch: u64,
    pub root: [u8; 32],
    pub total: u64,
    pub claimed: u64,
    pub claim_until: i64,
    pub bump: u8,
}

#[account]
#[derive(InitSpace)]
pub struct Receipt { pub bump: u8 }

#[derive(Accounts)]
#[instruction(epoch: u64)]
pub struct PostEpoch<'info> {
    #[account(mut)]
    pub authority: Signer<'info>, // treasury multisig
    pub mint: InterfaceAccount<'info, Mint>,
    #[account(init, payer = authority, space = 8 + Epoch::INIT_SPACE,
              seeds = [b"epoch", mint.key().as_ref(), &epoch.to_le_bytes()], bump)]
    pub epoch: Account<'info, Epoch>,
    #[account(token::mint = mint, token::authority = epoch)]
    pub vault: InterfaceAccount<'info, TokenAccount>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct Claim<'info> {
    #[account(mut)]
    pub holder: Signer<'info>,
    #[account(mut, has_one = mint)]
    pub epoch: Account<'info, Epoch>,
    pub mint: InterfaceAccount<'info, Mint>,
    #[account(mut, token::mint = mint, token::authority = epoch)]
    pub vault: InterfaceAccount<'info, TokenAccount>,
    #[account(mut, token::mint = mint, token::authority = holder)]
    pub holder_ata: InterfaceAccount<'info, TokenAccount>,
    #[account(init, payer = holder, space = 8 + Receipt::INIT_SPACE,
              seeds = [b"receipt", epoch.key().as_ref(), holder.key().as_ref()], bump)]
    pub receipt: Account<'info, Receipt>,
    pub token_program: Interface<'info, TokenInterface>,
    pub system_program: Program<'info, System>,
}

#[error_code]
pub enum DistError {
    #[msg("vault holds less than the epoch total")] Underfunded,
    #[msg("claim window closed")] Expired,
    #[msg("invalid merkle proof")] BadProof,
    #[msg("arithmetic overflow")] Overflow,
}
