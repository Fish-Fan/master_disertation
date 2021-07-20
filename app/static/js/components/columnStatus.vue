<template>
    <div>
        <el-tabs value="View">
        <el-tab-pane label="Column Profiling Result" name="View">
            <el-tag
                v-for="(item, key) in column_profiling_result_data"
                effect="dark"
                :type="item.type"
                style="margin: 10px 10px 5px 0"
            >
                {{ key }} : {{ item.value }}
            </el-tag>
        </el-tab-pane>
    </el-tabs>

    <div v-for="(pattern, index) in pattern_extract_data">
            <el-tag size="mini" type="warning">{{ pattern.pattern }}</el-tag>
            <el-progress
            :percentage="pattern.percentage"
            :color="computeStatusForProgressBar(index)"
            ></el-progress>
    </div>



    </div>
</template>

<script>
  module.exports = {
    props: ['column_profiling_result'],
    methods: {
        construct_profiling_result(message) {
            var tagObj = {};
            if ('missing_value' in message) {
                tagObj.p_missing = {
                    'value': this.roundUtil(message.missing_value) * 100 + '%',
                    'type': 'danger'
                };
            }
            if('valid' in message) {
                tagObj.valid = {
                    'value': this.roundUtil(message.valid) * 100 + '%',
                    'type': 'success'
                }
            }
            if ('distinct' in message) {
                tagObj.distinct = {
                    'value': this.roundUtil(message.distinct) * 100 + '%',
                    'type': 'success'
                }
            }
            if ('top_frequency' in message) {
                tagObj.top_frequency = {
                    'value': message.top_frequency,
                    'type': 'info'
                }
            }
            if ('max' in message) {
                tagObj.max = {
                    'value': message.max,
                    'type': 'warning'
                }
            }
            if ('min' in message) {
                tagObj.min = {
                    'value': message.min,
                    'type': 'warning'
                }
            }
            if ('mean' in message) {
                tagObj.mean = {
                    'value' : message.mean,
                    'type': 'warning'
                }
            }
            if ('median' in message) {
                tagObj.median = {
                    'value': message.median,
                    'type': 'warning'
                }
            }
            if ('zero' in message) {
                tagObj.zero = {
                    'value': message.zero,
                    'type': 'warning'
                }
            }
            if ('total' in message) {
                tagObj.total = {
                    'value': message.total,
                    'type': 'info'
                }
            }
            if ('constant' in message) {
                tagObj.constant = {
                    'value': message.constant,
                    'type': 'info'
                }
            }


            return tagObj;
        },
        roundUtil(num) {
            return Math.round(num * 10000) / 10000
        },
        computeStatusForProgressBar(index) {
            var color = '';
            switch(index) {
              case 0:
                color = "#67C23A";
                break;
              case 1:
                color = "#E6A23C";
                break;
              case 2:
                color = "#F56C6C";
                break;
            }
            return color
        },
        displayPattern(pattern) {
            return pattern.pattern;
        }
    },
    watch: {
      column_profiling_result: function(newVal, oldVal) {
          this.column_profiling_result_data = this.construct_profiling_result(newVal);
          if ('patterns_percentage' in newVal) {
              this.pattern_extract_data = newVal.patterns_percentage;
          } else {
              this.pattern_extract_data = [];
          }
      }
    },
    data() {
      return {
        column_profiling_result_data: {},
        pattern_extract_data: []
      }
    }
  }
</script>