"""
This is a module that allows you to connect to the Comscore library 
developed by Annalect and obtain synthesized information.
"""

__author__ = "Carlos Trujillo, Data analytics Manager"
__email__ = "carlos.trujillo@omnicommediagroup.com"
__status__ = "planning"


from sqlalchemy import create_engine
from pandas import read_sql, DataFrame
import pandas as pd

from collections import Counter

class comscore_omnicom_api:
    
    def __init__(self, user, password, endpoint = None):
        self.user = user
        self.password = password
        
        if isinstance(endpoint, type(None)):
     
            self.engine_str = 'postgresql://' + str(self.user) + ':' + str(self.password) + '@dsdk-v0p1-annalect.clf6bikxcquu.us-east-1.redshift.amazonaws.com:5439/dsdk'
        
        else:
            self.engine_str = 'postgresql://' + str(self.user) + ':' + str(self.password) + str(endpoint)
        
        self.engine = create_engine(self.engine_str)
        self.connection = self.engine.connect()
    
    def domain_by_time(self, country = None, start_date = None):
        
        query = """
        SELECT calendar_date as date, domain, event,
            count(distinct guid) as total_reach,
            count(guid) as total_visits, sum(time_spent) as total_time, total_time / total_visits as avg_time_per_visit
        
        FROM spectrum_comscore.clickstream_{country_in}
        where calendar_date >= {start_date_in}
        group by calendar_date, domain, event
        """
        
        if isinstance(country, type(None)):
            error = 'Define your country'
            raise TypeError(error)
        
        if isinstance(start_date, type(None)):
            start_date = '2019-01-01'
            print('The preset date was defined, which starts from January 1, 2019')
        
        setence = query.format(start_date_in = start_date, country_in = country)
        
        dataframe = read_sql(setence, con = self.connection)
        
        return dataframe

    def demographics_by_web(self, country = None, start_date = None):
        
        query = """
        SELECT main_base.domain, main_base.device, user_base.gender, 
               
                CASE
                    WHEN user_base.age > 13 AND user_base.age <= 17 THEN '13-17'
                    WHEN user_base.age > 17 AND user_base.age <= 34 THEN '18-34'
                    WHEN user_base.age > 34 AND user_base.age <= 54 THEN '35-54'
                    WHEN user_base.age > 54 THEN '55+'
                ELSE
                    'Undetermined'
                END
                AS age_group,
        
        
               user_base.children_present,
               count(distinct main_base.guid) as reach, count(main_base.guid) as visits, count(main_base.machine_id) as number_of_devices,
               sum(main_base.time_spent) as total_time, total_time / visits as avg_time_per_visit
               
               FROM spectrum_comscore.clickstream_{country_in} main_base
        
        LEFT JOIN
            (select person_id, gender, age, children_present
            from spectrum_comscore.person_demographics_{country_in}
            where date >= {start_date_in}
            group by person_id, gender, age, children_present) user_base
        
        ON main_base.guid = user_base.person_id
        
        where calendar_date >= {start_date_in}
        
        group by main_base.domain, main_base.device,
                user_base.gender, age_group, user_base.children_present
        """
        
        if isinstance(country, type(None)):
            error = 'Define your country'
            raise TypeError(error)
        
        if isinstance(start_date, type(None)):
            start_date = '2019-01-01'
            print('The preset date was defined, which starts from January 1, 2019')
        
        setence = query.format(start_date_in = start_date, country_in = country)
        
        dataframe = read_sql(setence, con = self.connection)
        dataframe.gender = dataframe.gender.astype(str).replace('nan', 'Undetermined')
        dataframe.children_present = dataframe.children_present.astype(str).replace('nan', 'Undetermined')
        
        return dataframe

    def demographics_by_web_density(self, country = None, start_date = None, domain = None):
        
        query = """
        SELECT main_base.domain, main_base.device, user_base.gender, user_base.age
        
        
               user_base.children_present,
               count(distinct main_base.guid) as reach, count(main_base.guid) as visits, count(main_base.machine_id) as number_of_devices,
               sum(main_base.time_spent) as total_time, total_time / visits as avg_time_per_visit
               
               FROM spectrum_comscore.clickstream_{country_in} main_base
        
        LEFT JOIN
            (select person_id, gender, age, children_present
            from spectrum_comscore.person_demographics_{country_in}
            where date >= {start_date_in}
            group by person_id, gender, age, children_present) user_base
        
        ON main_base.guid = user_base.person_id
        
        where calendar_date >= {start_date_in}
        and main_base.domain = '{domain_in}'
        
        group by main_base.domain, main_base.device,
                user_base.gender, user_base.age, user_base.children_present
        """
        
        if isinstance(country, type(None)):
            error = 'Define your country'
            raise TypeError(error)
        
        if isinstance(domain, type(None)):
            error = 'Define your domain'
            raise TypeError(error)
        
        if isinstance(start_date, type(None)):
            start_date = '2019-01-01'
            print('The preset date was defined, which starts from January 1, 2019')
        
        setence = query.format(start_date_in = start_date, country_in = country, domain_in = domain)
        
        dataframe = read_sql(setence, con = self.connection)
        dataframe.age = dataframe.age.astype(str).replace('nan', 'Undetermined')
        dataframe.gender = dataframe.gender.astype(str).replace('nan', 'Undetermined')
        dataframe.children_present = dataframe.children_present.astype(str).replace('nan', 'Undetermined')
        
        return dataframe

    
    def correlation_between_domains(self, country = None, start_date = None, url_site = None,
                                    domain_name = None, reach_greater_than = 8):
        query = """
        select calendar_date as date, domain, count(distinct guid) as reach, count(guid) as visits 
        from spectrum_comscore.clickstream_{country_in}
        where domain = '{url_site_in}' or domain like '%%{domain_name_in}%%'
        and calendar_date >= {start_date_in}
        group by date, domain
        having reach >= {reach_greater_than_in}
        
        UNION ALL
        
        select calendar_date as date, domain, count(distinct guid) as reach, count(guid) as visits 
        from spectrum_comscore.clickstream_{country_in}
        where guid in (select guid from spectrum_comscore.clickstream_{country_in}
                       where domain = '{url_site_in}' or domain like '%%{domain_name_in}%%'
                       group by guid)
        and calendar_date >= {start_date_in}
        and domain not in ('facebook.com', 'netflix.com', 'google.com', 'gmail.com', 'twitter.com', 'google.cl', 'instagram.com', 'youtube.com')
        group by date, domain
        having count(distinct guid) >= {reach_greater_than_in}
        """
        
        if isinstance(country, type(None)):
            error = 'Define your country'
            raise TypeError(error)
        if isinstance(domain_name, type(None)):
            error = 'Define the domain'
            raise TypeError(error)
        if isinstance(url_site, type(None)):
            error = 'Define the url of the site'
            raise TypeError(error)
            
        if isinstance(start_date, type(None)):
            start_date = '2019-01-01'
            print('The preset date was defined, which starts from January 1, 2019')
        
        dataframe = read_sql(query.format(country_in = country, start_date_in = start_date, 
                                        url_site_in = url_site, domain_name_in = domain_name,
                                        reach_greater_than_in = reach_greater_than),
                         con = self.connection)
        
        dataframe = dataframe.drop_duplicates().pivot(index='date', columns='domain', values='reach')
        dataframe_corr = dataframe.corr(method='pearson')
        dataframe_uniq_matrix = dataframe_corr[dataframe_corr.index.str.contains(domain_name)]
        
        return dataframe, dataframe_corr, dataframe_uniq_matrix
    
    def demographics_by_web_filtered(self, country = None, start_date = None, domain = None):
        
        query = """
        SELECT main_base.domain, main_base.device, user_base.gender, 
               
                CASE
                    WHEN user_base.age > 13 AND user_base.age <= 17 THEN '13-17'
                    WHEN user_base.age > 17 AND user_base.age <= 34 THEN '18-34'
                    WHEN user_base.age > 34 AND user_base.age <= 54 THEN '35-54'
                    WHEN user_base.age > 54 THEN '55+'
                ELSE
                    'Undetermined'
                END
                AS age_group,
        
        
               user_base.children_present,
               count(distinct main_base.guid) as reach, count(main_base.guid) as visits, count(main_base.machine_id) as number_of_devices,
               sum(main_base.time_spent) as total_time, total_time / visits as avg_time_per_visit
               
               FROM spectrum_comscore.clickstream_{country_in} main_base
        
        LEFT JOIN
            (select person_id, gender, age, children_present
            from spectrum_comscore.person_demographics_{country_in}
            where date >= {start_date_in}
            group by person_id, gender, age, children_present) user_base
        
        ON main_base.guid = user_base.person_id
        
        where calendar_date >= {start_date_in}
        and main_base.domain = '{domain_in}'
        
        group by main_base.domain, main_base.device,
                user_base.gender, age_group, user_base.children_present
        """
        
        if isinstance(country, type(None)):
            error = 'Define your country'
            raise TypeError(error)

        if isinstance(domain, type(None)):
            error = 'Define your domain'
            raise TypeError(error)
        
        if isinstance(start_date, type(None)):
            start_date = '2019-01-01'
            print('The preset date was defined, which starts from January 1, 2019')
        
        setence = query.format(start_date_in = start_date, country_in = country, domain_in = domain)
        
        dataframe = read_sql(setence, con = self.connection)
        dataframe.gender = dataframe.gender.astype(str).replace('nan', 'Undetermined')
        dataframe.children_present = dataframe.children_present.astype(str).replace('nan', 'Undetermined')
        
        return dataframe
    
    def domain_by_time_filtered(self, country = None, start_date = None, domain = None):
        
        query = """
        SELECT calendar_date as date, domain, event,
            count(distinct guid) as total_reach,
            count(guid) as total_visits, sum(time_spent) as total_time, total_time / total_visits as avg_time_per_visit
        
        FROM spectrum_comscore.clickstream_{country_in}
        where calendar_date >= {start_date_in} and domain = '{domain_in}'
        group by calendar_date, domain, event
        """
        
        if isinstance(country, type(None)):
            error = 'Define your country'
            raise TypeError(error)

        if isinstance(domain, type(None)):
            error = 'Define your domain'
            raise TypeError(error)

        if isinstance(start_date, type(None)):
            start_date = '2019-01-01'
            print('The preset date was defined, which starts from January 1, 2019')
        
        setence = query.format(start_date_in = start_date, country_in = country, domain_in = domain)
        
        dataframe = read_sql(setence, con = self.connection)
        
        return dataframe
 
    def overlaps_between_pages(self, country = None, start_date = None, domain = None,
                               competitors = None):
        
        testing = """
        select guid, domain
        from spectrum_comscore.clickstream_{country_in}
        where domain = '{domain_in}'
        and calendar_date >= {start_date_in}
        group by guid, domain
        
        UNION ALL
        
        
        select guid, domain
        from spectrum_comscore.clickstream_{country_in}
        where domain in {competidors_in}
        and calendar_date >= {start_date_in}
        group by guid, domain
        """
        
        if isinstance(country, type(None)):
            error = 'Define your country'
            raise TypeError(error)
        
        if isinstance(domain, type(None)):
            error = 'Define your domain'
            raise TypeError(error)
            
        if isinstance(competitors, type(None)):
            error = 'Define your competitors'
            raise TypeError(error)
        
        if not isinstance(competitors, tuple):
            error = 'Competitors must be entered in parentheses'
            raise TypeError(error)
            
        if isinstance(start_date, type(None)):
            start_date = '2019-01-01'
            print('The preset date was defined, which starts from January 1, 2019')
        
        tests = read_sql(testing.format(country_in = country, start_date_in = start_date, 
                                        domain_in = domain, competidors_in = competitors),
                         con = self.connection)
        
        #create unique list of names
        uniqueNames = tests.domain.unique()
        print(uniqueNames)
        
        #create a data frame dictionary to store your data frames
        DataFrameDict = {elem : pd.DataFrame for elem in uniqueNames}
        
        my_list = []
        
        for key in DataFrameDict.keys():
            DataFrameDict[key] = tests[:][tests.domain == key].reset_index(drop = True)
            my_list.append(list(tests[:][tests.domain == key].reset_index(drop = True).guid))
        
        frame = pd.DataFrame()
        
        for index in range(len(my_list)):
          lista_final = [list(filter(lambda x: x in my_list[index], sublist)) for sublist in my_list]
          
          mt = [len(x) / len(my_list[index]) for x in lista_final]
          frame = pd.concat([frame, DataFrame(mt)], axis = 1)
        
        frame.columns = list(uniqueNames)
        frame.index = list(uniqueNames)
        
        return DataFrameDict, frame
    
    def bayesian_inference_over_sites(self, country = None, domain = None, time_spent = None, start_date = None):
        
        query = """

        WITH my_table_3 as (
          select domain
            from spectrum_comscore.clickstream_{country_in}
              where guid in (select guid from spectrum_comscore.clickstream_{country_in} 
                              where domain = '{domain_in}' 
                              and calendar_date >= {start_date_in} 
                              and time_spent >= {time_spent_in}
                                group by guid)
              and time_spent >= {time_spent_in}
                group by domain
        ),
        
        my_table_4 as (
          select guid
            from spectrum_comscore.clickstream_{country_in}
              where guid in (select guid from spectrum_comscore.clickstream_{country_in} 
                              where domain = '{domain_in}' 
                              and calendar_date >= {start_date_in} 
                              and time_spent >= {time_spent_in}
                                group by guid)
                group by guid
        
        )
        
        SELECT domain, 'visitors' as type, count(distinct guid) as reach 
        from spectrum_comscore.clickstream_{country_in}
          where domain in (select domain from my_table_3) and guid in (select guid from my_table_4)
          and domain not in ('facebook.com', 'netflix.com', 'google.com', 'gmail.com', 'twitter.com', 'google.cl', 'instagram.com', 'youtube.com', 'bing.com', 'whatsapp.com', 'msn.com', 'live.com', '{domain_in}')
        group by 1,2
        
        UNION ALL
        
        SELECT domain, 'outsiders' as type, count(distinct guid) as reach 
        from spectrum_comscore.clickstream_{country_in}
          where domain in (select domain from my_table_3) and guid not in (select guid from my_table_4)
          and domain not in ('facebook.com', 'netflix.com', 'google.com', 'gmail.com', 'twitter.com', 'google.cl', 'instagram.com', 'youtube.com', 'bing.com', 'whatsapp.com', 'msn.com', 'live.com')
        group by 1,2

        """
        
        if isinstance(country, type(None)):
            error = 'Define your country'
            raise TypeError(error)
        
        if isinstance(domain, type(None)):
            error = 'Define your domain'
            raise TypeError(error)
            
        if isinstance(time_spent, type(None)):
            time_spent = 300
            print('The preset time_spent was defined, which 300 seconds')
    
        if isinstance(start_date, type(None)):
            start_date = '2019-01-01'
            print('The preset date was defined, which starts from January 1, 2019')
        
        
        
        table3 = read_sql(query.format(country_in = country, start_date_in = start_date, 
                                domain_in = domain, time_spent_in = time_spent
                                ), con = self.connection)
        
        pivot_table_3 = pd.pivot_table(table3, values = 'reach', index = 'type', columns = 'domain')
        
        dataframe_probs_a = pd.DataFrame(columns=['domain', 'p(a)', 'p(x | a)'])
        
        totals = pivot_table_3.iloc[0].sum() + pivot_table_3.iloc[1].sum()
        
        for indexs in range(pivot_table_3.shape[1]):
          dataframe_probs_a.loc[indexs] = [str(pivot_table_3.iloc[:,indexs].name), 
                                           pivot_table_3.iloc[:,indexs].sum() / totals, 
                                           pivot_table_3.iloc[:,indexs].visitors / pivot_table_3.iloc[:,indexs].sum()]
        
        dataframe_probs_a['p(a)*p(x | a)'] = dataframe_probs_a['p(a)'] * dataframe_probs_a['p(x | a)']
        dataframe_probs_a['bayes'] = dataframe_probs_a['p(a)*p(x | a)'] / dataframe_probs_a['p(a)*p(x | a)'].sum()
        dataframe_probs_a['bayes %'] = dataframe_probs_a['bayes'] * 100
        dataframe_probs_a.sort_values('bayes %', inplace=True)
        dataframe_probs_a.reset_index(drop = True, inplace = True)
        
        short_frame = dataframe_probs_a[dataframe_probs_a['bayes %'] > 0.4].reset_index(drop = True)
        
        return dataframe_probs_a, short_frame

    def bayesian_site_predictor(self, country = None, domain = None, time_spent = None, start_date = None):
        
        query_1 = """
        
        SELECT a.guid, concat(concat(b.domain,'_'),a.domain) AS trans_domain, b.positive_interval_time, b.timestamp_date_min, 
            min(a.visit_date_event) as min_visit
         
        
        FROM
        
            (select guid, domain, CONVERT(datetime,dateadd(s, event_time,'2000-01-01')) at time zone 'utc' at time zone 'clst' visit_date_event
            from spectrum_comscore.clickstream_{country_in}
            where guid in (select guid from spectrum_comscore.clickstream_{country_in} 
                   where domain = '{domain_in}' and calendar_date >= {start_date_in} and time_spent >= {time_spent_in}
                   group by guid) and time_spent >= 30
            group by guid, domain, event_time) a
        
        LEFT JOIN
        
        (select guid, domain, min(timestamp_date) as timestamp_date_min,
                    timestamp_date_min + INTERVAL '1 hour' as positive_interval_time
                from (
                    select guid, domain,
                       CONVERT(datetime, dateadd(s, event_time,'2000-01-01')) at time zone 'utc' at time zone 'clst' timestamp_date
                    from spectrum_comscore.clickstream_{country_in}
                    where domain = '{domain_in}' and calendar_date >= {start_date_in} and time_spent >= {time_spent_in}
                    ) group by guid, domain) b
        
        ON a.guid = b.guid
        
        where a.visit_date_event <= b.positive_interval_time and a.visit_date_event > b.timestamp_date_min
        
        group by 1,2,3,4
        
        having trans_domain not in ('{domain_in}_{domain_in}')
        
        """
        
        if isinstance(country, type(None)):
            error = 'Define your country'
            raise TypeError(error)
        
        if isinstance(domain, type(None)):
            error = 'Define your domain'
            raise TypeError(error)
            
        if isinstance(time_spent, type(None)):
            time_spent = 300
            print('The preset time_spent was defined, which 300 seconds')
    
        if isinstance(start_date, type(None)):
            start_date = '2019-01-01'
            print('The preset date was defined, which starts from January 1, 2019')
        
        tests = read_sql(query_1.format(country_in = country, start_date_in = start_date, 
                                        domain_in = domain, time_spent_in = time_spent
                                        ), con = self.connection)
        
        new = tests.sort_values(by = ['guid', 'min_visit'])
        new.drop_duplicates(subset = 'guid', keep = 'first', inplace = True)
        
        new['list_domains'] = new.trans_domain.str.split('_')
        
        list_of_domains = list(new['list_domains'])
        
        list_a = map(tuple, list_of_domains) #must convert to tuple because list is an unhashable type
        
        final_count = Counter(list_a)
        
        dataframe_of_visits = pd.DataFrame.from_dict(final_count, orient = 'index')
        
        dataframe_of_visits['other_index'] = dataframe_of_visits.index
        dataframe_of_visits.reset_index(inplace = True, drop = True)
        
        dataframe_of_visits['list'] = dataframe_of_visits.other_index.apply(list)
        dataframe_of_visits['list_str'] = dataframe_of_visits['list'].apply(','.join)
        dataframe_of_visits[['orig', 'desti']] = [sub.split(",") for sub in dataframe_of_visits.list_str]
        
        dataframe_of_visits['type'] = 'from_me_to_destiny' 
        
        dataframe_of_visits.columns = ['reach', 'indexs', 'list_index', 'list_index_str', 'orig', 'domain', 'type']
        final_a_frame = dataframe_of_visits[['domain', 'type', 'reach']]
        
        second_query = """
        
        SELECT a.guid, b.domain as orig, a.domain as desti, b.positive_interval_time, b.timestamp_date_min, min(a.visit_date_event) as min_visit
         
        
        FROM
        
            (select guid, domain, CONVERT(datetime,dateadd(s, event_time,'2000-01-01')) at time zone 'utc' at time zone 'clst' visit_date_event
            from spectrum_comscore.clickstream_{country_in}
            where guid in (select guid from spectrum_comscore.clickstream_{country_in} 
                   where domain in {domain_in} and calendar_date >= {start_date_in} and time_spent >= {time_spent_in}
                   group by guid) and time_spent >= 30
            group by guid, domain, event_time) a
        
        LEFT JOIN
        
        (select guid, domain, min(timestamp_date) as timestamp_date_min,
                    timestamp_date_min + INTERVAL '1 hour' as positive_interval_time
                from (
                    select guid, domain,
                       CONVERT(datetime, dateadd(s, event_time,'2000-01-01')) at time zone 'utc' at time zone 'clst' timestamp_date
                    from spectrum_comscore.clickstream_{country_in}
                    where domain in {domain_in} and calendar_date >= {start_date_in} and time_spent >= {time_spent_in}
                    ) group by guid, domain) b
        
        ON a.guid = b.guid
        
        where a.visit_date_event <= b.positive_interval_time and a.visit_date_event > b.timestamp_date_min
        and a.domain != b.domain
        
        group by 1,2,3,4,5
        
        """
        
        optilist = list(dataframe_of_visits.domain)
        strings = ','.join(optilist)
        my_tuple = tuple(strings.split(','))
        
        second_frame_test = read_sql(second_query.format(country_in = country, start_date_in = start_date, 
                                        domain_in = my_tuple, time_spent_in = time_spent
                                        ), con = self.connection)

        to_my_domain = second_frame_test[second_frame_test.desti == domain]
        
        new = to_my_domain.sort_values(by = ['guid', 'min_visit']).reset_index(drop = True)
        new.drop_duplicates(subset = 'guid', keep = 'first', inplace = True)
        new['trans_domain'] = new.orig + '_' + new.desti
        
        new['list_domains'] = new.trans_domain.str.split('_')
        
        list_of_domains = list(new['list_domains'])
        
        list_a = map(tuple, list_of_domains) #must convert to tuple because list is an unhashable type
        
        final_count = Counter(list_a)
        
        dataframe_of_visits_to_me = pd.DataFrame.from_dict(final_count, orient = 'index')
        
        dataframe_of_visits_to_me['other_index'] = dataframe_of_visits_to_me.index
        dataframe_of_visits_to_me.reset_index(inplace = True, drop = True)
        
        dataframe_of_visits_to_me['list'] = dataframe_of_visits_to_me.other_index.apply(list)
        dataframe_of_visits_to_me['list_str'] = dataframe_of_visits_to_me['list'].apply(','.join)
        dataframe_of_visits_to_me[['orig', 'desti']] = [sub.split(",") for sub in dataframe_of_visits_to_me.list_str]
        
        dataframe_of_visits_to_me['type'] = 'from_domains_to_me'
        
        dataframe_of_visits_to_me.columns = ['reach', 'indexs', 'list_index', 'list_index_str', 'domain', 'desti', 'type']
        final_b_frame = dataframe_of_visits_to_me[['domain', 'type', 'reach']]

        to_others_domain = second_frame_test[second_frame_test.desti != domain]
        
        new = to_others_domain.sort_values(by = ['guid', 'min_visit']).reset_index(drop = True)
        new.drop_duplicates(subset = 'guid', keep = 'first', inplace = True)
        new['trans_domain'] = new.orig + '_' + new.desti
        
        new['list_domains'] = new.trans_domain.str.split('_')
        
        list_of_domains = list(new['list_domains'])
        
        list_a = map(tuple, list_of_domains) #must convert to tuple because list is an unhashable type
        
        final_count = Counter(list_a)
        
        dataframe_of_visits_to_others = pd.DataFrame.from_dict(final_count, orient = 'index')
        
        dataframe_of_visits_to_others['other_index'] = dataframe_of_visits_to_others.index
        dataframe_of_visits_to_others.reset_index(inplace = True, drop = True)
        
        dataframe_of_visits_to_others['list'] = dataframe_of_visits_to_others.other_index.apply(list)
        dataframe_of_visits_to_others['list_str'] = dataframe_of_visits_to_others['list'].apply(','.join)
        dataframe_of_visits_to_others[['orig', 'desti']] = [sub.split(",") for sub in dataframe_of_visits_to_others.list_str]
        
        dataframe_of_visits_to_others['type'] = 'from_domains_to_others'
        
        dataframe_of_visits_to_others.columns = ['reach', 'indexs', 'list_index', 'list_index_str', 'orig', 'domain', 'type']
        final_c_frame = dataframe_of_visits_to_others[['domain', 'type', 'reach']]

        final_frame = pd.concat([final_a_frame, final_b_frame, final_c_frame])
        
        pivot_table_3 = pd.pivot_table(final_frame, values = 'reach', index = 'type', columns = 'domain').fillna(0)
        
        dataframe_probs_a = pd.DataFrame(columns=['domain', 'p(a)', 'split'])

        totals = pivot_table_3.iloc[0].sum() + pivot_table_3.iloc[1].sum() + pivot_table_3.iloc[2].sum()
        
        for indexs in range(pivot_table_3.shape[1]):
            dataframe_probs_a.loc[indexs] = [str(pivot_table_3.iloc[:,indexs].name), 
                                            pivot_table_3.iloc[:,indexs].sum() / totals, 
                                            pivot_table_3.iloc[:,indexs].from_me_to_destiny / pivot_table_3.iloc[:,indexs].sum()]
        
        dataframe_probs_a['p(X)'] = dataframe_probs_a['p(a)'] * dataframe_probs_a['split']
        dataframe_probs_a['bayes'] = (dataframe_probs_a['p(a)'] * dataframe_probs_a['split']) / dataframe_probs_a['p(X)'].sum()
        dataframe_probs_a['bayes %'] = dataframe_probs_a['bayes'] * 100
        
        dataframe_probs_a.sort_values('bayes %', inplace=True)
        dataframe_probs_a.reset_index(drop = True, inplace = True)
        
        short_frame_a = dataframe_probs_a[dataframe_probs_a['bayes %'] > 0.4].reset_index(drop = True)
        
        return short_frame_a, dataframe_probs_a