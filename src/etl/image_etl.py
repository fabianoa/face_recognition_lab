import apache_beam as beam

from apache_beam.options.pipeline_options import PipelineOptions

from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText

p = beam.Pipeline(options=PipelineOptions())

class GetTotal(beam.DoFn):
    def process(self, element):
        # get the total transactions for one item
        return [(str(element[0]), sum(element[1]))]

data_from_source = (p
                    | 'ReadMyFile' >> ReadFromText('./input/BreadBasket_DMS.csv')
                    | 'Splitter using beam.Map' >> beam.Map(lambda record: (record.split(','))[0])
                    | 'Map record to 1' >> beam.Map(lambda record: (record, 1))
                    | 'GroupBy the data' >> beam.GroupByKey()
                    | 'Get the total in each day' >> beam.ParDo(GetTotal())
                    | 'Export results to new file' >> WriteToText('output/day-list', '.txt')
                    )

result = p.run()