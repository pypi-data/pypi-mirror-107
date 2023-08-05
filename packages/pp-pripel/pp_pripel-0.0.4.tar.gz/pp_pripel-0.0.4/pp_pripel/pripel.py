import os
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.log.exporter.xes import factory as xes_exporter
from pp_pripel.tracematcher import TraceMatcher as TraceMatcher
from pp_pripel.attributeAnonymizier import AttributeAnonymizier as AttributeAnonymizier
from pp_pripel.trace_variant_query import privatize_tracevariants
import datetime


class PRIPEL():

    def __init__(self):
        self = self


    def apply(self, log_path, epsilon, N, k, result_log_path=""):

        try:
            if result_log_path == "":
                now = datetime.datetime.now()
                date_time = now.strftime(" %m-%d-%y %H-%M-%S ")
                head, tail = os.path.split(log_path)
                log_name = tail.replace(".xes", "")
                new_ending = "PRIPEL" + date_time + log_name + "_epsilon_" + str(epsilon) + "_k" + str(k) + "_N"+ str(N) + ".xes"
                result_log_path = os.path.join(head, new_ending)

            starttime = datetime.datetime.now()
            log = xes_import_factory.apply(log_path)

            starttime_tv_query = datetime.datetime.now()
            tv_query_log = privatize_tracevariants(log, epsilon, k, N)
            print(len(tv_query_log))
            endtime_tv_query = datetime.datetime.now()
            print("Time of TV Query: " + str((endtime_tv_query - starttime_tv_query)))
            starttime_trace_matcher = datetime.datetime.now()
            traceMatcher = TraceMatcher(tv_query_log, log)
            matchedLog = traceMatcher.matchQueryToLog()
            print(len(matchedLog))
            endtime_trace_matcher = datetime.datetime.now()
            print("Time of TraceMatcher: " + str((endtime_trace_matcher - starttime_trace_matcher)))
            distributionOfAttributes = traceMatcher.getAttributeDistribution()
            occurredTimestamps, occurredTimestampDifferences = traceMatcher.getTimeStampData()
            print(min(occurredTimestamps))
            starttime_attribute_anonymizer = datetime.datetime.now()
            attributeAnonymizier = AttributeAnonymizier()
            anonymiziedLog, attritbuteDistribution = attributeAnonymizier.anonymize(matchedLog, distributionOfAttributes,
                                                                                    epsilon, occurredTimestampDifferences,
                                                                                    occurredTimestamps)
            endtime_attribute_anonymizer = datetime.datetime.now()
            print("Time of attribute anonymizer: " + str(endtime_attribute_anonymizer - starttime_attribute_anonymizer))
            xes_exporter.export_log(anonymiziedLog, result_log_path)
            endtime = datetime.datetime.now()
            print("Complete Time: " + str((endtime - starttime)))

            print("Time of TV Query: " + str((endtime_tv_query - starttime_tv_query)))
            print("Time of TraceMatcher: " + str((endtime_trace_matcher - starttime_trace_matcher)))
            print("Time of attribute anonymizer: " + str(endtime_attribute_anonymizer - starttime_attribute_anonymizer))

            print(result_log_path)
            print(self.freq(attritbuteDistribution))

        except Exception as e:
            return {'code':1, 'msg':str(e)}

        return {'code':0, 'msg': 'success'}

    def freq(self,lst):
        d = {}
        for i in lst:
            if d.get(i):
                d[i] += 1
            else:
                d[i] = 1
        return d