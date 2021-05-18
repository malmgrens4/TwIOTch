from twitchio.dataclasses import Message


def parse_args(msg: Message, kwords: [str]):
    args = msg.content.split()[1:]
    arg_dict = {}
    for i, kword in enumerate(kwords):
        if i >= len(args):
            arg_dict[kword] = None
        else:
            arg_dict[kword] = args[i]

    return arg_dict
