"""Main module."""

import modules.arbitrary_miner as arbminer
import modules.julia_miner as julieminer
import modules.language as language
import modules.python_miner as pyminer
import modules.repo_miner as repo_miner
import modules.r_miner as rminer
import modules.utilities as util
import os



def examine(url):
  dict_list = None

  repo_miner.clone_repo(url)
  repo_name = os.path.splitext(os.path.basename(url))[0]

  lang = language.detect_language('tmp')

  if (lang == '.py'):
    dict_list = pyminer.PyRepoMiner('tmp', repo_name).yaml_dict
  elif (lang == '.R'):
    dict_list= rminer.RRepoMiner('tmp', repo_name).yaml_dict
  elif (lang == '.jl'):
    dict_list = julieminer.JuliaRepoMiner('tmp', repo_name).yaml_dict
  else:
    dict_list = arbminer.ArbitraryRepoMiner('tmp', repo_name, lang).yaml_dict

  owner_info = repo_miner.extract_owner(url, 'tmp')
  dict_list.insert(1, dict(owner=owner_info))

  about_desc = repo_miner.extract_about(url, 'tmp', repo_name)
  dict_list.insert(2, dict(about=about_desc))

  repo_miner.delete_repo()

  return util.yaml_dump(dict_list)