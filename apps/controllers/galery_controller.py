import os
import pdb
import json
from posixpath import split

def get_list():
  command = """near call nftattootest.testnet nft_tokens --accountId nftattootest.testnet --depositYocto 1"""
  out = os.popen(command).read()
  #res = out.replace("\n","")[out.find('['):-1]
  res = out[out.find('['):-1]
  res_list = []
  split_res = res.replace("\n","").split("},  {")
  #pdb.set_trace()
  res_list.append(json.loads(json.dumps(split_res[0][1:] + "}")))
  for meta_data in split_res[1:-1]: res_list.append(json.loads(json.dumps("{" + meta_data + "}")))
  #pdb.set_trace()
  res_list.append(json.loads(json.dumps("{" + split_res[-1][:-1])))
  for meta in res_list: print(meta) 
  #pdb.set_trace()
  json_res = json.loads(res)
  return (json_res)
