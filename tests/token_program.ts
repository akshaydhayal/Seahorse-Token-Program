import * as anchor from "@project-serum/anchor";
import { Program } from "@project-serum/anchor";
import { TokenProgram } from "../target/types/token_program";

describe("token_program", () => {
  // Configure the client to use the local cluster.
  anchor.setProvider(anchor.AnchorProvider.env());

  const program = anchor.workspace.TokenProgram as Program<TokenProgram>;

  it("Is initialized!", async () => {
    // Add your test here.
    const tx = await program.methods.initialize().rpc();
    console.log("Your transaction signature", tx);
  });
});
