<template>
    <el-form ref="form">
      <el-form-item :label="rule.label">
            <!-- List of operands (optional) -->
      <el-select
        v-model="userField"
      >
        <el-option v-for="(field, idx) in fields"
                   :label="field"
                   :value="field"
                   :key="idx"></el-option>
      </el-select>

      <!-- List of operators (e.g. =, !=, >, <) -->
      <el-select
        v-model="operator"
      >
        <el-option v-for="(operator, idx) in operators"
                   :key="idx"
                   :label="operator"
                   :value="operator">
        </el-option>
      </el-select>

      <!-- Basic text input -->
      <el-input
        v-model="userAttribute"
        type="text"
      ></el-input>

      </el-form-item>
    </el-form>
</template>

<script>
  module.exports = {
    props: ["value"],
    computed: {
      fields() {
        return ["email", "username", "first_name", "last_name"];
      },
      operators() {
        return ["equals", "starts_with", "ends_with", "contains"];
      },
      userField: {
        get() {
          return this.value.field;
        },
        set(field) {
          this.$emit("input", {
            ...this.value,
            field
          });
        }
      },
      operator: {
        get() {
          return this.value.operator;
        },
        set(operator) {
          this.$emit("input", {
            ...this.value,
            operator
          });
        }
      },
      userAttribute: {
        get() {
          return this.value.value;
        },
        set(userAttribute) {
          this.$emit("input", {
            ...this.value,
            value: userAttribute
          });
        }
      }
    }

  }
</script>
