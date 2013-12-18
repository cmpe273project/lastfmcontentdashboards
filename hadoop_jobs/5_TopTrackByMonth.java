
import java.io.IOException;
import java.util.Iterator;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.FileInputFormat;
import org.apache.hadoop.mapred.FileOutputFormat;
import org.apache.hadoop.mapred.JobClient;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reducer;
import org.apache.hadoop.mapred.Reporter;
import org.apache.hadoop.mapred.TextInputFormat;
import org.apache.hadoop.mapred.TextOutputFormat;

public class sample {

  public static class Map extends MapReduceBase implements Mapper<LongWritable, Text, Text, LongWritable> {

	private Text MonthOfYear = new Text();
    private final static LongWritable one = new LongWritable(1);

    public void map(LongWritable key, Text value, OutputCollector<Text, LongWritable> output, Reporter reporter) throws IOException {
 //Emitting Track Names and one from 1k dataset for each year
    	{
			try{
				String[] split = value.toString().split("\t");

			  MonthOfYear.set(split[1].toString().substring(5,7));
		   	  output.collect(MonthOfYear,one);

			}catch (NumberFormatException e) {
			}
		}

}

 public static class Reduce extends MapReduceBase implements Reducer<Text, LongWritable, Text, LongWritable> {


 public void reduce(Text key, Iterator<LongWritable> values, OutputCollector<Text, LongWritable> output, Reporter reporter) throws IOException {
      int sum = 0;

     while (values.hasNext()) {
    	  sum=(int) (sum+values.next().get());
    	   }
      output.collect(key, new LongWritable(sum));
    }
  }

  public static void main(String[] args) throws Exception {
    JobConf conf = new JobConf(TopTrackNamesYearWise.class);

    conf.setJobName("5_TopTrackByMonth");

    conf.setOutputKeyClass(Text.class);
    conf.setOutputValueClass(LongWritable.class);

    conf.setMapperClass(Map.class);
    conf.setReducerClass(Reduce.class);

    conf.setInputFormat(TextInputFormat.class);
    conf.setOutputFormat(TextOutputFormat.class);

    FileInputFormat.setInputPaths(conf, new Path(args[0]));
    FileOutputFormat.setOutputPath(conf, new Path(args[1]));

    JobClient.runJob(conf);
  }
  }
  }
