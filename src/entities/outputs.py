import json
import csv
from xml.etree.ElementTree import ElementTree, TreeBuilder, indent
import yaml
from entities.workers import Workers, Worker
from entities.positions import Positions


class Outputs:
    workers: Workers
    positions: Positions

    def __init__(self, workers:Workers, positions:Positions) -> None:
        self.workers = workers
        self.positions = positions


    def all_sers(self) -> None:
        self.json_ser()
        self.csv_ser()
        self.xml_ser()
        self.yaml_ser()


    def json_ser(self) -> None:
        with open('out/data.json', 'w') as f: f.write('')
        data = []
        for worker in self.workers.workers:
            rights = [{'uuid': right.uuid, 'name': right.name, 'description': right.description} for right in worker.position.rights]
            position = {'uuid': worker.position.uuid, 'name': worker.position.name, 'description': worker.position.description, 'rights': rights}
            data.append({'uuid': worker.uuid, 'sex': worker.sex, 'name': worker.name, 'birthday': worker.birthday, 'position': position})
        with open('out/data.json', 'a', encoding='UTF-8') as f:
            json.dump(data, f, indent='    ', ensure_ascii=False)
        return None


    def csv_ser(self) -> None:
        with open('out/data.csv', 'w') as f: f.write('')
        data = []
        for worker in self.workers.workers:
            rights = [[str(right.uuid), right.name, right.description] for right in worker.position.rights]
            position = [worker.position.uuid, worker.position.name, worker.position.description]
            for right in rights: position.extend(right)
            data.append([worker.uuid, worker.sex, worker.name, worker.birthday, *position])
        with open('out/data.csv', 'a', encoding='UTF-8') as f:
            writer = csv.writer(f)
            writer.writerow(['uuid','sex','name','birthday','position.uuid','position.name','position.description','right.uuid','right.name','right.description','...'])
            writer.writerows(data)
        return None


    def xml_ser(self) -> None:
        with open('out/data.xml', 'w') as f: f.write('')
        data = []
        for worker in self.workers.workers:
            rights = {}
            for right in worker.position.rights:
                rights[f'right_{right.uuid}'] = {'uuid': right.uuid, 'name': right.name, 'description': right.description}
            position = {'uuid': worker.position.uuid, 'name': worker.position.name, 'description': worker.position.description, 'rights': rights}
            data.append({'uuid': worker.uuid, 'sex': worker.sex, 'name': worker.name, 'birthday': worker.birthday, 'position': position})
        builder = TreeBuilder()
        builder.start('workers', {})
        for worker in data:
            self.xml_recur_pars(builder, worker)
        tree = ElementTree(builder.close())
        indent(tree, space='    ')
        tree.write('out/data.xml', encoding='UTF-8', xml_declaration=True)
        return None


    def xml_recur_pars(self, builder:TreeBuilder, data) -> None:
        if not isinstance(data, dict): return builder.data(str(data))
        if isinstance(data, list): [builder.data(el) for el in data]
        else:
            for key in data:
                keystr = key.split('_', maxsplit=1)[0]
                builder.start(keystr, {})
                self.xml_recur_pars(builder, data[key])
                builder.end(keystr)


    def yaml_ser(self) -> None:
        with open('out/data.yaml', 'w') as f: f.write('')
        with open('out/data.yaml', 'a', encoding='UTF-8') as f:
            yaml.dump_all(self.workers.workers, f, indent=4, allow_unicode=True)
