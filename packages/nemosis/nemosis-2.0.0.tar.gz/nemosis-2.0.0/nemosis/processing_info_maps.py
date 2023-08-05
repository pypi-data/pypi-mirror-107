import os

from nemosis import filters, downloader, query_wrapers, write_file_names, date_generators


setup = {'DISPATCHLOAD': None,
         'TRADINGLOAD': None,
         'TRADINGPRICE': None,
         'TRADINGREGIONSUM': None,
         'TRADINGINTERCONNECT': None,
         'DISPATCHPRICE': None,
         'DISPATCH_UNIT_SCADA': None,
         'DISPATCHCONSTRAINT': None,
         'DUDETAILSUMMARY': None,
         'DUDETAIL': None,
         'GENCONDATA': None,
         'SPDREGIONCONSTRAINT': None,
         'SPDCONNECTIONPOINTCONSTRAINT': None,
         'SPDINTERCONNECTORCONSTRAINT': None,
         'FCAS_4_SECOND': None,
         'ELEMENTS_FCAS_4_SECOND': None,
         'VARIABLES_FCAS_4_SECOND': None,
         'Generators and Scheduled Loads': None,
         'BIDDAYOFFER_D': query_wrapers.dispatch_date_setup,
         'BIDPEROFFER_D': None,
         'FCAS_4s_SCADA_MAP': None,
         'DISPATCHINTERCONNECTORRES': None,
         'DISPATCHREGIONSUM': None,
         'LOSSMODEL': None,
         'LOSSFACTORMODEL': None,
         'MNSP_DAYOFFER': query_wrapers.dispatch_date_setup,
         'MNSP_PEROFFER': query_wrapers.dispatch_half_hour_setup,
         'MNSP_INTERCONNECTOR': None,
         'INTERCONNECTOR': None,
         'INTERCONNECTORCONSTRAINT': None,
         'MARKET_PRICE_THRESHOLDS': None}

search_type = {'DISPATCHLOAD': 'start_to_end',
               'TRADINGLOAD': 'start_to_end',
               'TRADINGPRICE': 'start_to_end',
               'TRADINGREGIONSUM': 'start_to_end',
               'TRADINGINTERCONNECT': 'start_to_end',
               'DISPATCHPRICE': 'start_to_end',
               'DISPATCH_UNIT_SCADA': 'start_to_end',
               'DISPATCHCONSTRAINT': 'start_to_end',
               'DUDETAILSUMMARY': 'end',
               'DUDETAIL': 'all',
               'GENCONDATA': 'all',
               'SPDREGIONCONSTRAINT': 'all',
               'SPDCONNECTIONPOINTCONSTRAINT': 'all',
               'SPDINTERCONNECTORCONSTRAINT': 'all',
               'FCAS_4_SECOND': 'start_to_end',
               'ELEMENTS_FCAS_4_SECOND': None,
               'VARIABLES_FCAS_4_SECOND': None,
               'Generators and Scheduled Loads': None,
               'BIDDAYOFFER_D': 'start_to_end',
               'BIDPEROFFER_D': 'start_to_end',
               'FCAS_4s_SCADA_MAP': None,
               'DISPATCHINTERCONNECTORRES': 'start_to_end',
               'DISPATCHREGIONSUM': 'start_to_end',
               'LOSSMODEL': 'all',
               'LOSSFACTORMODEL': 'all',
               'MNSP_DAYOFFER': 'start_to_end',
               'MNSP_PEROFFER': 'start_to_end',
               'MNSP_INTERCONNECTOR': 'all',
               'INTERCONNECTOR': 'all',
               'INTERCONNECTORCONSTRAINT': 'all',
               'MARKET_PRICE_THRESHOLDS': 'all'}

filter = {'DISPATCHLOAD': filters.filter_on_settlementdate,
          'TRADINGLOAD': filters.filter_on_settlementdate,
          'TRADINGPRICE': filters.filter_on_settlementdate,
          'TRADINGREGIONSUM': filters.filter_on_settlementdate,
          'TRADINGINTERCONNECT': filters.filter_on_settlementdate,
          'DISPATCHPRICE': filters.filter_on_settlementdate,
          'DISPATCH_UNIT_SCADA': filters.filter_on_settlementdate,
          'DISPATCHCONSTRAINT': filters.filter_on_settlementdate,
          'DUDETAILSUMMARY': filters.filter_on_start_and_end_date,
          'DUDETAIL': filters.filter_on_effective_date,
          'GENCONDATA': filters.filter_on_effective_date,
          'SPDREGIONCONSTRAINT': filters.filter_on_effective_date,
          'SPDCONNECTIONPOINTCONSTRAINT': filters.filter_on_effective_date,
          'SPDINTERCONNECTORCONSTRAINT': filters.filter_on_effective_date,
          'FCAS_4_SECOND': filters.filter_on_timestamp,
          'ELEMENTS_FCAS_4_SECOND': None,
          'VARIABLES_FCAS_4_SECOND': None,
          'Generators and Scheduled Loads': None,
          'BIDDAYOFFER_D': filters.filter_on_settlementdate,
          'BIDPEROFFER_D': filters.filter_on_interval_datetime,
          'FCAS_4s_SCADA_MAP': None,
          'DISPATCHINTERCONNECTORRES': filters.filter_on_settlementdate,
          'DISPATCHREGIONSUM': filters.filter_on_settlementdate,
          'LOSSMODEL': filters.filter_on_effective_date,
          'LOSSFACTORMODEL': filters.filter_on_effective_date,
          'MNSP_DAYOFFER': filters.filter_on_settlementdate,
          'MNSP_PEROFFER': filters.filter_on_date_and_peroid,
          'MNSP_INTERCONNECTOR': filters.filter_on_effective_date,
          'INTERCONNECTOR': filters.filter_on_last_changed,
          'INTERCONNECTORCONSTRAINT': filters.filter_on_effective_date,
          'MARKET_PRICE_THRESHOLDS': filters.filter_on_effective_date}

finalise = {'DISPATCHLOAD': None,
            'TRADINGLOAD': None,
            'TRADINGPRICE': None,
            'TRADINGREGIONSUM': None,
            'TRADINGINTERCONNECT': None,
            'DISPATCHPRICE': None,
            'DISPATCH_UNIT_SCADA': None,
            'DISPATCHCONSTRAINT': [query_wrapers.convert_genconid_effectivedate_to_datetime_format],
            'DUDETAILSUMMARY': [query_wrapers.most_recent_records_before_start_time,
                                query_wrapers.drop_duplicates_by_primary_key],
            'DUDETAIL': [query_wrapers.most_recent_records_before_start_time,
                                query_wrapers.drop_duplicates_by_primary_key],
            'GENCONDATA': [query_wrapers.most_recent_records_before_start_time,
                           query_wrapers.drop_duplicates_by_primary_key],
            'SPDREGIONCONSTRAINT': [query_wrapers.most_recent_records_before_start_time],
            'SPDCONNECTIONPOINTCONSTRAINT': [query_wrapers.most_recent_records_before_start_time,
                                             query_wrapers.drop_duplicates_by_primary_key],
            'SPDINTERCONNECTORCONSTRAINT': [query_wrapers.most_recent_records_before_start_time,
                                            query_wrapers.drop_duplicates_by_primary_key],
            'FCAS_4_SECOND': [query_wrapers.fcas4s_finalise],
            'ELEMENTS_FCAS_4_SECOND': None,
            'VARIABLES_FCAS_4_SECOND': None,
            'Generators and Scheduled Loads': None,
            'BIDDAYOFFER_D': None,
            'BIDPEROFFER_D': None,
            'FCAS_4s_SCADA_MAP': None,
            'DISPATCHINTERCONNECTORRES': None,
            'DISPATCHREGIONSUM': None,
            'LOSSMODEL': [query_wrapers.most_recent_records_before_start_time,
                              query_wrapers.drop_duplicates_by_primary_key],
            'LOSSFACTORMODEL': [query_wrapers.most_recent_records_before_start_time,
                              query_wrapers.drop_duplicates_by_primary_key],
            'MNSP_DAYOFFER': [query_wrapers.most_recent_records_before_start_time,
                              query_wrapers.drop_duplicates_by_primary_key],
            'MNSP_PEROFFER': [query_wrapers.most_recent_records_before_start_time,
                              query_wrapers.drop_duplicates_by_primary_key],
            'MNSP_INTERCONNECTOR': [query_wrapers.most_recent_records_before_start_time,
                                    query_wrapers.drop_duplicates_by_primary_key],
            'INTERCONNECTOR': [query_wrapers.most_recent_records_before_start_time,
                               query_wrapers.drop_duplicates_by_primary_key],
            'INTERCONNECTORCONSTRAINT': [query_wrapers.most_recent_records_before_start_time,
                                         query_wrapers.drop_duplicates_by_primary_key],
            'MARKET_PRICE_THRESHOLDS': None}

date_gen = {'MMS': date_generators.year_and_month_gen,
            'FCAS': date_generators.year_month_day_index_gen}

write_filename = {'MMS': write_file_names.write_file_names,
                  'FCAS': write_file_names.write_file_names_fcas}

downloader = {'MMS': downloader.run,
              'FCAS': downloader.run_fcas4s}
