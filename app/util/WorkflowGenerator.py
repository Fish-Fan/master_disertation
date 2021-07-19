from datetime import datetime
import json

class WorkflowGenerator():
    count = 1

    def generator(self, removeColumns, dateTime, dateTimeColumnsIdx, filename):
        ans = {}
        id = 'task' + datetime.now().strftime('%Y%m%d%H%M%s')
        ans['id'], ans['name'] = id, id
        ans['nodes'] = self._getNodes_(removeColumns, dateTime, dateTimeColumnsIdx, filename)
        ans['links'] = self._linkNodes_(ans.get('nodes'))
        return json.dumps(ans)

    def _getNodes_(self, removeColumns, dateTime, dateTimeColumnsIdx, filename):
        nodes = []
        nodes.append(self._getReadNode_(filename))
        if removeColumns:
            nodes.append(self._getRemoveNode_(removeColumns))
        if dateTime:
            if 'date' in dateTime:
                nodes.append(self._getDayOfWeekNode_(dateTimeColumnsIdx))
            if 'time' in dateTime:
                nodes.append(self._getHourOfDayNode_(dateTimeColumnsIdx))

        end_node = nodes[-1]
        end_node['is_end'] = 1
        return nodes

    def _getReadNode_(self, filename):
        node = {}
        node['id'] = 'node' + str(self.count)
        node['name'] = 'read'
        node['ports'] = [{
            "name": "filename",
            "value": filename
        }]
        node['ui'] = self._getPosition_()
        node['spec_id'] = 'pyflow.read'
        self.count += 1
        return node

    def _getRemoveNode_(self, removeColumnsArr):
        removeColumns = ""
        for s in removeColumnsArr:
            removeColumns += s
            removeColumns += ','
        removeColumns = removeColumns[:-1]
        node = {}
        node['id'] = 'node' + str(self.count)
        node['name'] = 'remove'
        node['ports'] = [{
            "name": "cname",
            "value": removeColumns
        }]
        node['ui'] = self._getPosition_()
        node['spec_id'] = 'pyflow.remove'
        self.count += 1
        return node

    def _getDayOfWeekNode_(self, dateTimeColumnsIdx):
        node = {}
        node['id'] = 'node' + str(self.count)
        node['name'] = 'day_of_week'
        node['ports'] = [{
            "name": "i",
            "value": str(dateTimeColumnsIdx)
        }]
        node['ui'] = self._getPosition_()
        node['spec_id'] = 'pyflow.day_of_week'
        self.count += 1
        return node

    def _getHourOfDayNode_(self, dateTimeColumnsIdx):
        node = {}
        node['id'] = 'node' + str(self.count)
        node['name'] = 'hour_of_day'
        node['ports'] = [{
            "name": "i",
            "value": str(dateTimeColumnsIdx)
        }]
        node['ui'] = self._getPosition_()
        node['spec_id'] = 'pyflow.hour_of_day'
        self.count += 1
        return node

    def _getPosition_(self):
        position = {}
        position['x'] = str(self.count * 100) + 'px'
        position['y'] = str(self.count * 100) + 'px'
        return position

    def _linkNodes_(self, nodes):
        links = []
        if len(nodes) <= 1:
            return links

        for i in range(1, len(nodes)):
            link = {}
            link['source'] = nodes[i - 1].get('id') + ':out'
            link['target'] = nodes[i].get('id') + ':data'
            links.append(link)
        return links

if __name__ == '__main__':
    removeColumnsArr = ['ClassVolume6', 'ClassVolume5']
    removeColumns = ""
    for s in removeColumnsArr:
        removeColumns += s
        removeColumns += ','
    removeColumns = removeColumns[:-1]
    dateTime = {'date': True, 'time': True}
    dateTimeColumnsIdx = 0
    filename = 'traffic_data.csv'
    ge = WorkflowGenerator()
    str = ge.generator(removeColumns, dateTime, dateTimeColumnsIdx, filename)
    print(str)