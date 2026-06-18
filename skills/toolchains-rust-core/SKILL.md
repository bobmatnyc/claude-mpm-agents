---
name: toolchains-rust-core
description: Core Rust toolchain conventions — ownership/borrowing patterns, error handling, async with tokio, and idiomatic project structure for the rust-engineer agent
version: 1.0.0
category: toolchain
toolchain: rust
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Idiomatic Rust 2024 conventions: ownership/borrowing, Result-based error handling with thiserror/anyhow, async with tokio, and project structure. The rust-engineer agent defers pattern decisions to this skill."
    when_to_use: "Loaded by the rust-engineer agent for any Rust implementation, refactor, or review task."
    quick_start: "Borrow by default, own when you must. Return Result, never panic in library code. Use tokio for async I/O. Run cargo fmt + cargo clippy -- -D warnings before declaring done."
context_limit: 700
tags:
  - rust
  - rust-2024
  - ownership
  - borrowing
  - async
  - tokio
  - idiomatic
  - toolchain
requires_tools: []
---

# Rust Core Toolchain Conventions

## Edition and Toolchain

- Target **Rust 2024 edition**. MSRV is set by the most-constrained transitive dependency,
  not the edition floor — pin it explicitly in `Cargo.toml` (`rust-version = "..."`).
- Gate every change on `cargo fmt --check`, `cargo clippy -- -D warnings`, and `cargo test`.
- Prefer `cargo nextest run` for faster, isolated test execution when available.

## Ownership and Borrowing

- **Borrow by default, own only when necessary.** Accept `&str` / `&[T]` in function
  signatures, not `String` / `Vec<T>`, unless the function must take ownership.
- Return owned values; let callers borrow. Avoid returning references tied to locals.
- Reach for `Cow<'_, str>` when a value is usually borrowed but occasionally owned.
- Use `Rc`/`Arc` only for genuine shared ownership; prefer passing references first.
- Interior mutability: `Cell`/`RefCell` for single-threaded, `Mutex`/`RwLock` (under `Arc`)
  for shared-state concurrency. Never hold a lock across an `.await`.

## Error Handling

- **Never `unwrap()`/`expect()`/`panic!` in library code.** Return `Result<T, E>`.
- Libraries: define a typed error enum with `thiserror`. Applications: `anyhow::Result`
  with `.context(...)` to add provenance at each boundary.
- Use the `?` operator for propagation; convert errors with `From`/`#[from]`.
- Reserve `panic!` for truly unreachable invariants, and document why.

## Async with tokio

- Use `#[tokio::main]` (or an explicit runtime) and `async`/`.await` for I/O-bound work.
- Spawn concurrent work with `tokio::spawn`; join with `tokio::join!` or `try_join!`.
- Apply explicit timeouts via `tokio::time::timeout` on all external calls.
- Offload CPU-bound work with `tokio::task::spawn_blocking` — never block the runtime.
- Hold no `std::sync` lock across an `.await`; use `tokio::sync` primitives instead.

## Project Structure and Idioms

- One responsibility per module; expose a curated public API via `pub` in `lib.rs`.
- Derive `Debug`, and `Clone`/`PartialEq`/`Eq` where cheap and meaningful.
- Model state with enums + exhaustive `match`; avoid boolean-flag soup.
- Prefer iterator chains over manual index loops; they are clearer and often faster.
- Use newtypes (`struct UserId(u64)`) to make illegal states unrepresentable.
- Write doctests for public functions; they double as runnable documentation.
