import { EventEmitter } from "node:events";
import type { SystemEvent } from "@pepebot/protocol";

/** In-process event bus with a small history buffer for /status. */
export class EventBus {
  private ee = new EventEmitter();
  private history: SystemEvent[] = [];

  constructor(private readonly keep = 50) {}

  publish(e: SystemEvent): void {
    this.history.push(e);
    if (this.history.length > this.keep) this.history.shift();
    this.ee.emit("event", e);
  }

  subscribe(fn: (e: SystemEvent) => void): () => void {
    this.ee.on("event", fn);
    return () => this.ee.off("event", fn);
  }

  recent(): SystemEvent[] {
    return [...this.history];
  }
}
