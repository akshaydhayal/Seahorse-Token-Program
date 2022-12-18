This project was created by Seahorse 0.2.5.

# Seahorse Token Program
The Objective of this project is to create a **Lottery smart contract** where users can buy lottery tickets and a random winner will be selected from all participants and lottery prize will be rewarded to the winner.

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
