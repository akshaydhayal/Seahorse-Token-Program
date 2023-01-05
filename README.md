This project was created by Seahorse 0.2.5.

# Seahorse Token Program
The Objective of this tutorial is to get started with **SPL Tokens** with seahorse. We will learn about TokenMints and TokenAccounta and how to use them to mint tokens, transfer tokens to other user's TokenAccount. SPL-Tokens represent all non-native tokens on the Solana network. Both fungible and non-fungible tokens (NFTs) on Solana are SPL-Tokens.

## Prerequisites
We need to install some command line tools for this project to build. We need [Solana](https://docs.solana.com/cli/install-solana-cli-tools), [Anchor](https://project-serum.github.io/anchor/getting-started/installation.html#install-rust), [NodeJS](https://nodejs.org/en/) and [Seahorse](https://seahorse-lang.org/docs/installation). The links provided contain the step-by-step guide on installing these tools and the dependencies required for them like Rust.

You can check if package got installed correctly by running command like :

`solana -V`
`anchor -V`
`seahorse -V`

For this project, the version used are :
* anchor 0.25.0

* seahorse v0.2.5

* node 19.0.0

## Getting started with Seahorse
We initialize Seahorse Project using command `seahorse init token_program`. This will create a project directory with multiple files which is mostly similar to anchor projects, just will write our seahorse program in `token_program/programs_py/token_program.py`

## Involved Accounts
Under the hood, the Toke Program in Solana Program Library (SPL) is used. It contains instructions for creating and interacting with SPL-Tokens. These tokens represent all non-native (i.e. not SOL) tokens on the Solana network. 

The 3 parties involved in this token programms are :
* The **Token Program** contains instructions for creating and interacting with SPL-Tokens
* **Token Mints** are accounts which hold data about a specific Token, but do not hold Tokens
* **Token Accounts** are used to hold Tokens of a specific Token Mint

<p align="center">
  <img src="https://github.com/akshaydhayal/Seahorse-Token-Program/blob/master/assets/tokenProgram0.png" alt="Alt text" title="Optional title" height="420" width="550">
</p>


## Program Instructions
We have 4 functions/instructions in this Program. Let's understand all the different Program instructions one by one.

### 1. initTokenMint
When someone wants to create a new token, we have to use something create-token function to initialize a new Mint Account. `initTokenMint` is the function where we create our TokenMint Accounts. TokenMint account contains the following informations: 
* `mint-authority` which is a public-key (pubkey) authorized to mint this token
*  the number of `decimals` of the token etc. 
```
def init_token_mint(new_token_mint: Empty[TokenMint], signer: Signer):
  new_token_mint.init(
    payer = signer,
    seeds = ['token-mint', signer],
    decimals = 0,
    authority = signer
  )
  ```
This account stores general information about the token and who has permissions over it.We can see the particular details about our TokenMint such as the addresses of the mint,mint authority, and the decimal precision of the token. 

Observe that there is no data about token holdings of particular individuals. These are stored in Token Accounts.
<p align="center">
  <img src="https://github.com/akshaydhayal/Seahorse-Token-Program/blob/master/assets/figg1.png" alt="Alt text" title="Optional title" height="180" width="550">
</p>


### 2. initTokenAccount
A Token Account holds tokens of a specific "mint" and has a specified "owner" of the account. Ownership relationships become a bit confusing, though. The token account itself is owned by the Token program and it is the Token program who controls access to these tokens using the owner, and delegate fields within the account. The owner is the pubkey who can spend/transfer the tokens, and the owner can give rights to a delegate pubkey to spend up to a delegatedAmount of tokens. Only the owner is authorized to decrease the Token Account balance (transfer, burn, etc.) while anyone can send tokens to the Token Account to increase its balance.

The TokenAccount has number of fields like:
* mint - this is the mint whose tokens this this account will hold
* authority - the account that has authority over this account
```
def init_token_account(new_token_account: Empty[TokenAccount],recipient: Empty[TokenAccount],
                       mint: TokenMint,signer: Signer):
  new_token_account.init(payer = signer, seeds = ['token-account1', signer],
                         mint = mint, authority = signer)
  recipient.init(payer = signer, seeds = ['token-account2', signer],
                         mint = mint, authority = signer)
```
<p align="center">
  <img src="https://github.com/akshaydhayal/Seahorse-Token-Program/blob/master/assets/figg2.png" alt="Alt text" title="Optional title" height="150" width="740">
</p>

<p float="left">
  <img src="https://github.com/akshaydhayal/Seahorse-Token-Program/blob/master/assets/figg3.png" width="460" height="185"/> 
  <img src="https://github.com/akshaydhayal/Seahorse-Token-Program/blob/master/assets/figg4.png" width="460" height="185"/>
</p>
We can create Associated TokenAccounts also. An Associated Token Account is a Token Account where the address of the Token Account is derived using an owner's public key and a token mint. Associated Token Accounts provide a deterministic way to find the Token Account owned by a specific publicKey for a specific token mint. You can create it like: 

```
  new_token_account.init( payer = signer, mint = mint, 
  authority = signer, associated = True )
 ```

### 3. useTokenMint
Minting tokens is the process of issuing new tokens into circulation. When you mint tokens, you increase the supply of the token mint and deposit the newly minted tokens into a token account. Only the mint authority of a token mint is allowed to mint new tokens.
This process updates both, the user’s balance (in the token-account) and the supply (in the mint account). 
<p align="center">
  <img src="https://github.com/akshaydhayal/Seahorse-Token-Program/blob/master/assets/figg6.png" alt="Alt text" title="Optional title" height="250" width="800">
</p>
<p align="center">
  <img src="https://github.com/akshaydhayal/Seahorse-Token-Program/blob/master/assets/figg5.png" alt="Alt text" title="Optional title" height="140" width="850">
</p>

```
def use_token_mint(mint: TokenMint,recipient: TokenAccount,signer: Signer):
  mint.mint(authority = signer,
    to = recipient,
    amount = u64(3000)
  )
  ```
  
  Additionally, we can burn some parts of minted tokens also. Burning tokens is the process of decreasing the token supply of a given token mint. Burning tokens removes them from the given token account and from broader circulation.Like below, we are burning 1000 tokens from the `recipient` account from his 3000 minted tokens above (so after this instruction, recipient` will gain exactly 2000 token.)
  But recipient_signer` must be the authority for the `recipient` token account.
  ```
    mint.burn( authority = recipient_signer,
    holder = recipient, amount = 1000
  )
  ```

### 4. useTokenAccount

This function is used to transfer tokens from one tockenAccount to the other.SPL-Token transfers require both the sender and receiver to have token accounts for the mint of the tokens being transferred. The tokens are transferred from the sender’s token account to the receiver’s token account.
<p align="center">
  <img src="https://github.com/akshaydhayal/Seahorse-Token-Program/blob/master/assets/figg8.png" alt="Alt text" title="Optional title" height="250" width="800">
</p>

```
def use_token_account(signer_account: TokenAccount, recipient: TokenAccount,signer: Signer):
  signer_account.transfer( authority = signer,
    to = recipient, amount = 100 )
```
We have transferred 100 tokens from signer_account to recipient tokenAccount. After transfer, the token balances of both TokenAccounts will be 2900 and 100 tokens repectively.
<p align="center">
  <img src="https://github.com/akshaydhayal/Seahorse-Token-Program/blob/master/assets/figg7.png" alt="Alt text" title="Optional title" height="180" width="850">
</p>  





