#!/bin/bash
ID=perich.testnet
near view $ID nft_tokens_for_owner '{"account_id": "'alice.$ID'"}'
