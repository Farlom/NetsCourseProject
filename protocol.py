import settings


def serialize(player: bool, data: tuple) -> str:
    if player:
        return f'{data[0]:02d}{data[1]:02d}{data[2]:02d}0'
    else:
        return f'0000{data[0]:02d}{data[1]}'


def deserialize(player: bool, data):
    if player:
        return int(data[4:6])
    else:
        return int(data[0:2]), int(data[2:4]), int(data[4:6]), bool(int(data[6:7]))



