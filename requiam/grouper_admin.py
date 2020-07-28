import requests
import pandas as pd

from .commons import figshare_stem


class GrouperAPI:

    def __init__(self, grouper_host, grouper_base_path, grouper_user, grouper_password):

        self.grouper_host = grouper_host
        self.grouper_base_dn = grouper_base_path
        self.grouper_user = grouper_user
        self.grouper_password = grouper_password

        self.endpoint = 'https://{}/{}'.format(grouper_host, grouper_base_path)
        self.headers = {'Content-Type': 'text/x-json'}

    def get_group_list(self, group_type):
        """Retrieve list of groups in a Grouper stem"""

        if group_type not in ['portal', 'quota', '']:
            raise ValueError("Incorrect [group_type] input")

        grouper_group = figshare_stem(group_type)

        params = dict()
        params['WsRestFindGroupsRequest'] = {'wsQueryFilter':
                                                 {'queryFilterType': 'FIND_BY_STEM_NAME',
                                                  'stemName': grouper_group}}

        rsp = requests.post(self.endpoint, auth=(self.grouper_user, self.grouper_password),
                            json=params, headers=self.headers)

        return rsp.json()

    def check_group_exists(self, group, group_type):
        """Check whether a Grouper group exists within a Grouper stem"""

        if group_type not in ['portal', 'quota']:
            raise ValueError("Incorrect [group_type] input")

        if group_type:
            grouper_group = figshare_stem('portal')

        result = self.get_group_list(group_type)

        group_df = pd.DataFrame(result['WsFindGroupsResults']['groupResults'])

        df_query = group_df.loc[group_df['displayExtension'] == group]
        status = True if not df_query.empty else False
        return status



