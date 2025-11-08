class Powers:
    power_list: list[str]
    power_uuids: list[dict]
    power_names: dict[str, dict]
    max_power_num: int

    def __init__(self, names, descriptions):
        self.power_list = names
        bits = len(names)
        self.max_power_num = 2**bits - 1
        for uuid in range(bits):
            self.power_uuids.append({"uuid": uuid+1, "name": names[uuid], "description": descriptions[uuid]})
            self.power_names[names[uuid]] = {"uuid": uuid+1, "name": names[uuid], "description": descriptions[uuid]}

    def get(self, name:str) -> dict:
        return isinstance(name, str) and self.power_names[name] # type: ignore
    
    def getbyuuid(self, uuid:int) -> dict:
        return isinstance(uuid, int) and self.power_uuids[uuid-1] # type: ignore

    def ispowervalid(self, powers:int) -> bool:
        return isinstance(powers, int) and powers >= 1 and powers <= self.max_power_num
