"""
Methods about git.
"""
import git
import os
from functools import lru_cache
from typing import Tuple
from git import Repo, Commit

from lumo.utils.keys import FN, CFG
from lumo.utils.paths import repo_dir, compare_path

bin_file = ['*.pth', '*.npy', '*.ckpt',
            '*.ft',  # for feather
            '*.pkl'
            ]

lib_gitignores = ['.lumo/',
                  '*.lumo.*',
                  '.data',
                  '.datas',
                  '.dataset',
                  '.datasets',
                  ] + bin_file

py_gitignore = "\n".join(['# Byte-compiled / optimized / DLL files',
                          '__pycache__/', '*.py[cod]',
                          '*$py.class',
                          '# C extensions', '*.so',
                          '# Distribution / packaging',
                          '.Python', 'build/', 'develop-eggs/', 'dist/', 'downloads/', 'eggs/', '.eggs/',
                          'lib/', 'lib64/', 'parts/', 'sdist/', 'var/', 'wheels/', 'pip-wheel-metadata/',
                          'share/python-wheels/', '*.egg-info/', '.installed.cfg', '*.egg', 'MANIFEST',
                          '', '# PyInstaller',
                          '#  Usually these files are written by a python script from a template',
                          '#  before PyInstaller builds the exe, so as to inject date/other infos into '
                          'it.',
                          '*.manifest', '*.spec',
                          '# Installer logs', 'pip-log.txt',
                          'pip-delete-this-directory.txt',
                          '# Unit test / coverage reports',
                          'htmlcov/', '.tox/', '.nox/', '.coverage', '.coverage.*', '.cache',
                          'nosetests.xml', 'coverage.xml', '*.cover', '.hypothesis/', '.pytest_cache/',
                          '# Translations', '*.mo', '*.pot',
                          '# Django stuff:', '*.log', 'local_settings.py', 'db.sqlite3',
                          '# Flask stuff:',
                          'instance/', '.webassets-cache', '', '# Scrapy stuff:', '.scrapy', '',
                          '# Sphinx documentation', 'docs/_build/', '', '# PyBuilder', 'target/', '',
                          '# Jupyter Notebook', '.ipynb_checkpoints', '',
                          '# IPython',
                          'profile_default/', 'ipython_config.py',
                          '# pyenv', '.python-version', '',
                          '# celery beat schedule file', 'celerybeat-schedule', '',
                          '# SageMath parsed files', '*.sage.py', '',
                          '# Environments', '.env', '.venv',
                          'env/', 'venv/', 'ENV/', 'env.bak/', 'venv.bak/', '',
                          '# Spyder project settings', '.spyderproject', '.spyproject', '',
                          '# Rope project settings', '.ropeproject', '',
                          '# mkdocs documentation',
                          '/site', '',
                          '# mypy',
                          '.mypy_cache/', '.dmypy.json', 'dmypy.json',
                          '# Pyre type checker', '.pyre/'] + lib_gitignores)


def check_have_commit(repo: Repo):
    if len(repo.heads) == 0:
        repo.git.add('.')
        repo.index.commit('initial commit')


def check_gitignore(repo: Repo, force=False):
    """
    check if file `.gitignore`  have the needed ignored items for lumo.
    """
    version_mark = os.path.join(repo.working_dir, FN.VERSION)
    ignorefn = os.path.join(repo.working_dir, '.gitignore')

    if os.path.exists(version_mark) and not force:
        if os.path.exists(ignorefn):
            return False

    old_marks = [f for f in os.listdir(repo.working_dir) if f.startswith('.lumo.')]
    for old_mark in old_marks:
        mark_fn = os.path.join(repo.working_dir, old_mark)
        if os.path.isfile(mark_fn):
            os.remove(mark_fn)

    with open(version_mark, 'w') as w:
        pass

    if not os.path.exists(ignorefn):
        with open(ignorefn, 'w', encoding='utf-8') as w:
            w.write(py_gitignore)
        return True
    else:
        amend = False
        with open(ignorefn, 'r', encoding='utf-8') as r:
            lines = [i.strip() for i in r.readlines()]
            for item in lib_gitignores:
                if item not in lines:
                    lines.append(item)
                    amend = True
        if amend:
            with open(ignorefn, 'w', encoding='utf-8') as w:
                w.write('\n'.join(lines))

    return amend


def git_config_syntax(value: str) -> str:
    """
    syntax value(especially file path) which will be stored in git config
    """
    return value.replace('\\\\', '/').replace('\\', '/')


class branch:
    """
    用于配合上下文管理切换 git branch

    with branch(repo, branch):
        repo.index.commit('...')
    """

    def __init__(self, repo: Repo, branch: str):
        self.repo = repo
        self.old_branch = self.repo.head.reference
        self.branch = branch

    def __enter__(self):
        if self.branch not in self.repo.heads:
            head = self.repo.create_head(self.branch)
        else:
            head = self.repo.heads[self.branch]

        self.repo.head.reference = head
        # self.repo.head.reset(index=True, working_tree=True)
        return head

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.repo.head.reference = self.old_branch


def init_repo(dir='./') -> Tuple[Repo, bool]:
    """
    initialize a directory, including git init, lumo config and a initial commit.
    """
    path = repo_dir(dir, ignore_info=True)
    init = False
    if path is not None and compare_path(path, dir):
        repo = Repo(path)
    else:
        repo = Repo.init(dir)
        init = True

    if check_gitignore(repo=repo, force=True):
        repo.git.add('.')
        repo.index.commit('initial commit')
        init = True

    check_have_commit(repo)
    return repo, init


@lru_cache()
def load_repo(dir='./') -> Repo:
    """
    Try to load git repository object of a directory.
    Args:
        dir: str, a directory path, default is the current working dir.
        if dir is a repository dir, then a git.Repo object will be retured.
        if not, some you can type a path to init it, or type '!' to cancel init it.

    Returns:
        git.Repo object or None if dir not have git repository and cancel to init it.
    """

    path = repo_dir(dir)

    if path is None:
        if CFG.STATE.OS_NAME.DISABLE_GIT not in os.environ:
            print("fatal: not a git repository (or any of the parent directories)")
            print("-----------------------")
            path = input("type root path to init this project, \n(default: {}, type '!' to ignore".format(os.getcwd()))
        else:
            print("Variable 'repo' will be a None object. "
                  "Any operation that need this repo may cause Exception.")
            return None

        if '!' in path or '！' in path:
            print("Variable 'repo' will be a None object. "
                  "Any operation that need this repo may cause Exception.")
            return None

        repo = Repo.init(path)
        check_gitignore(repo=repo, force=True)
        repo.git.add('.')
        repo.index.commit('initial commit')
    else:
        repo = Repo(path)
        amend = check_gitignore(repo=repo, force=False)
        if amend:
            repo.git.add('.gitignore')
            repo.index.commit('fix gitignore')
    check_have_commit(repo)
    return repo


_commits_map = {}


def commit(repo: Repo = None, key=None, branch_name=CFG.BRANCH_NAME, info: str = None) -> Commit:
    """
    ```
        TODO behavior need to be verified.
        cd <repo working dir>
        git reset <branch_name>
        git add .
        git commit -m "<info>"
        git reset <original branch>
    ```
    Args:
        repo:
        key:
            to avoid duplicate commit, a key value can be passed,
            commit operation will be perform if `key` hasn't appeared before.
            default value is None, means you can commit as you want without limitation
        branch_name:
            commit on which branch, nonexistent branch will be created.
        info:
            commit info, a string
    Returns:
        git.Commit object, see gitpython for details.
    """
    try:
        if repo is None:
            repo = load_repo()

        if key is not None and key in _commits_map:
            return _commits_map[key]

        with branch(repo, branch_name):
            repo.git.add(all=True)
            commit_info = '[[EMPTY]]'
            if info is not None:
                commit_info = info
            commit_ = repo.index.commit(commit_info)
        if key is not None:
            _commits_map[key] = commit_
    except git.GitCommandError:
        commit_ = None
    return commit_


def reset(commit):
    """
    TODO
    将工作目录中的文件恢复到某个commit
    恢复快照的 git 流程:
        git branch experiment
        git add . & git commit -m ... // 保证文件最新，防止冲突报错，这一步由 Experiment() 代为完成
        git checkout <commit-id> // 恢复文件到 <commit-id>
        git checkout -b reset // 将当前状态附到新的临时分支 reset 上
        git branch experiment // 切换回 experiment 分支
        git add . & git commit -m ... // 将当前状态重新提交到最新
            // 此时experiment 中最新的commit 为恢复的<commit-id>
        git branch -D reset  // 删除临时分支
        git branch master // 最终回到原来分支，保证除文件变动外git状态完好
    Returns:
        An Experiment represents this reset operation
    """
    commit = commit

    old_path = os.getcwd()
    os.chdir(commit.tree.abspath)
    exp = Experiment('Reset')

    repo = self.repo
    from thexp.utils.repository import branch
    with branch(commit.repo, _GITKEY.thexp_branch) as new_branch:
        repo.git.checkout(commit.hexsha)
        repo.git.checkout('-b', 'reset')
        repo.head.reference = new_branch
        repo.git.add('.')
        ncommit = repo.index.commit("Reset from {}".format(commit.hexsha))
        repo.git.branch('-d', 'reset')
    exp.add_plugin('reset', {
        'test_name': self.name,  # 从哪个状态恢复
        'from': exp.commit.hexsha,  # reset 运行时的快照
        'where': commit.hexsha,  # 恢复到哪一次 commit，是恢复前的保存的状态
        'to': ncommit.hexsha,  # 对恢复后的状态再次进行提交，此时 from 和 to 两次提交状态应该完全相同
    })

    exp.end()
    os.chdir(old_path)
    return exp


def archive(commit):
    """
    TODO
    将某次 test 对应 commit 的文件打包，相关命令为
        git archive -o <filename> <commit-hash>
    Returns:
        An Experiment represents this archive operation
    """

    old_path = os.getcwd()
    os.chdir(commit.tree.abspath)
    exp = Experiment('Archive')

    revert_path = exp.makedir('archive')
    revert_fn = os.path.join(revert_path, "code.zip")
    exp.add_plugin('archive', {'file': revert_fn,
                               'test_name': self.name})
    with open(revert_fn, 'wb') as w:
        self.repo.archive(w, commit)

    exp.end()
    os.chdir(old_path)
    return exp
