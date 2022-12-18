# token_program
# Built with Seahorse v0.2.5

from seahorse.prelude import *

declare_id('Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS')


@instruction
def init_token_account(new_token_account: Empty[TokenAccount],recipient: Empty[TokenAccount],
                       mint: TokenMint,signer: Signer):
  # On top of the regular init args, you need to provide:
  #   - the mint that this token account will hold tokens of
  #   - the account that has authority over this account.
  new_token_account.init(payer = signer, seeds = ['token-account1', signer],
                         mint = mint, authority = signer)
  recipient.init(payer = signer, seeds = ['token-account2', signer],
                         mint = mint, authority = signer)
  
@instruction
def use_token_account(signer_account: TokenAccount, recipient: TokenAccount,signer: Signer):
  # Transfers 100 tokens from `signer_account` to `recipient`.
  # `signer` must be the authority (owner) for `signer_token_account`.
  # Note that the amounts here are in *native* token quantities - you need to
  # account for decimals when you make calls to .transfer().
  
  print("Before transfer reciever token : ",recipient.amount, "Sender token : ",signer_account.amount)
  signer_account.transfer( authority = signer,
    to = recipient, amount = 100 )

  print("After transfer reciever token : ",recipient.amount, "Sender token : ",signer_account.amount)



@instruction
def init_token_mint(new_token_mint: Empty[TokenMint], signer: Signer):
  # On top of the regular init args, you need to provide:
  #   - the number of decimals that this token will have
  #   - the account that has authority over this account.
  new_token_mint.init(
    payer = signer,
    seeds = ['token-mint', signer],
    decimals = 0,
    authority = signer
  )
  
@instruction
def use_token_mint(mint: TokenMint,recipient: TokenAccount,signer: Signer):
  # Mint 100 tokens from our `mint` to `recipient`.
  # `signer` must be the authority (owner) for `mint`.
  # Note that the amounts here are in *native* token quantities - you need to
  # account for decimals when you make calls to .mint().
  print("Before mint Owner token : ",recipient.amount)
  mint.mint(
    authority = signer,
    to = recipient,
    amount = u64(3000)
  )
  print("After mint Owner token : ",recipient.amount)



#initTokenMint ----->  initTokenAccount ---->    useTokenMint      ------>    useTokenAccount