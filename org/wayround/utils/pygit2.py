
"""
some handy utilities for pygit2
"""

import pygit2


class NotATree(Exception):
    pass


def listdir(repo, ref, path):

    tree = get_object(repo, ref, path)

    ret = None

    if not isinstance(tree, pygit2.Tree):
        raise NotATree("Not a tree: {}".format(path))
    else:
        ret = []

        for i in tree:
            ret.append(i.name)

    return ret


def get_object(repo, ref, path):

    ret = ref.peel(pygit2.GIT_OBJ_TREE)

    if path not in [None, '']:

        elem = ret[path]
        ret = repo[elem.oid]

    return ret


def get_file_last_change_commit(repo, ref, path):
    # return get_file_commits_with_unic_oids(repo, ref, path)[-1][0]

    comm = ref.peel(pygit2.GIT_OBJ_COMMIT)
    tree = comm.tree

    ret = comm

    for i in repo.walk(ret.oid, pygit2.GIT_SORT_TIME):
        if not path in i.tree:
            ret = None
            break

        if ret is not None:
            if i.tree[path].oid != ret.tree[path].oid:
                break

        ret = i

    return ret


def get_branch_commits(repo, ref):

    ret = []

    for i in repo.walk(
            ref.peel(pygit2.GIT_OBJ_COMMIT).oid,
            pygit2.GIT_SORT_TIME
            ):
        ret.append(i)

    return ret


def get_file_commits(repo, ref, path):

    # oid = ref.peel(pygit2.GIT_OBJ_TREE)[path].oid

    coid = []

    for i in repo.walk(
            ref.peel(pygit2.GIT_OBJ_COMMIT).oid,
            pygit2.GIT_SORT_TIME
            ):
        if path in i.tree:
            coid.append((i, i.tree[path].oid))
        else:
            coid.append((i, None))

    return coid


def get_file_commits_with_unic_oids(repo, ref, path):

    res = get_file_commits(repo, ref, path)

    cur_oid = None

    for i in range(len(res) - 1, -1, -1):
        tup = res[i]

        if cur_oid != tup[1]:
            cur_oid = tup[1]
        else:
            del res[i]

    return res
