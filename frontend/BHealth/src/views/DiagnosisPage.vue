<template>
  <div class="DiagnosisPage">
    <el-tabs type="border-card" class="demo-tabs">
      <el-tab-pane v-for="item in diagnosis" :key="item.id" :label="item.id">
        <div class="display-area" ref="displayContent">
          <div class="medical-record">
            <h1>计算机学院BHealth医院</h1>
            <div class="document">
              <!-- Name, Gender, Age on the same line -->
              <div class="patient-info">
                <p><strong>姓名：</strong>{{ item.content.name }}</p>
                <p><strong>性别：</strong>{{ item.content.gender }}</p>
                <p><strong>年龄：</strong>{{ item.content.age }}</p>
                <p><strong>就诊科室：</strong>{{ item.content.department }}</p>
              </div>
              <!-- Horizontal line with spacing -->
              <hr class="divider" />
              <p><strong>就诊病号：</strong>{{ item.content.recordNumber }}</p>
              <p><strong>就诊时间：</strong>{{ item.content.visitTime }}</p>
              <p><strong>联系电话：</strong>{{ item.content.phone }}</p>
              <p><strong>家庭住址：</strong>{{ item.content.address }}</p>
              <p><strong>主诉：</strong>{{ item.content.complaint }}</p>
              <p><strong>现病史：</strong>{{ item.content.currentHistory }}</p>
              <p><strong>既往史：</strong>{{ item.content.medicalHistory }}</p>
              <p><strong>过敏史：</strong>{{ item.content.allergyHistory }}</p>
              <p><strong>诊断：</strong>{{ item.content.diagnosis }}</p>
              <p><strong>处方：</strong>{{ item.content.content }}</p>
              <p><strong>药品：</strong>
                <ul>
                  <li v-for="(drug, index) in item.content.takenDrugs" :key="index">
                    药品:{{ drug.name }}, 每日用量:{{ drug.count }}
                  </li>
                </ul>
              </p>
              <p><strong>建议：</strong>{{ item.content.advice }}</p>
            </div>
            <div class="signature">
              医师签字：{{item.content.doctorName}} &nbsp;手签：
            </div>
          </div>
          </div>
<!--      <el-button type="primary" @click="exportToPDF" class="pdfButton">导出为 PDF</el-button>-->
      </el-tab-pane>
      <el-tab-pane v-if="diagnosis.length === 0" label="0">
        <div class="display-area" ref="displayContent">
          <div class="medical-record">
            <h1>计算机学院BHealth医院</h1>
            <div class="document">
              <p>暂无诊断书</p>
            </div>
          </div>
        </div>
      </el-tab-pane>
  </el-tabs>
  </div>
</template>

<script lang="ts" setup>
import {useRoute} from "vue-router";
import {onMounted, ref} from "vue";
import api from "@/api";
import {ElMessage} from "element-plus";
import html2pdf from 'html2pdf.js';

const displayContent = ref(null);


const exportToPDF = () => {
  html2pdf().from(displayContent.value).save('病例信息.pdf');
};

const diagnosisIds = ref([]);
const diagnosis = ref([]);

const getPatient = async (patientId) => {
  console.log(patientId.value);
  if (patientId.value <= 0) {
    ElMessage.error('请输入正确的病人编号');
    return;
  }
  const res = await api.getPatientInfoById({patient_id : patientId});
  diagnosisIds.value = res.diagnosis;
  await getDiagnosis();
}

onMounted(() => {
  const $route = useRoute();
  const patientId = $route.params.id;
  getPatient(patientId);
})

const getDiagnosis = async () => {
  console.log(diagnosisIds.value.length);
  for (let i = 0; i < diagnosisIds.value.length; i++) {
    const res = await api.getDiagnosis({diagnosis_id : diagnosisIds.value[i]});
    let content = res.content
    content = content.replace(/'/g, '"') // 将所有单引号替换为双引号
    .replace(/"\s*"\s*:\s*"/g, '":"') // 处理多余的引号
    .replace(/\\"/g, '"') // 处理转义字符
    console.log(content);

    res.content = JSON.parse(content);
    diagnosis.value.push(res);
    content = '';
  }
  console.log(diagnosis.value);
}
</script>

<style scoped>
.DiagnosisPage{
  padding: 20px;
  margin: 5% auto 0;
  width: 1350px;
}

.demo-tabs > .el-tabs__content {
  padding: 32px;
  color: #6b778c;
  font-size: 32px;
  font-weight: 600;
}
.demo-tabs .custom-tabs-label .el-icon {
  vertical-align: middle;
}
.demo-tabs .custom-tabs-label span {
  vertical-align: middle;
  margin-left: 4px;
}

.editCase {
  width: 1350px;
  margin: 100px auto 0;
}

.display-area {
  padding: 20px;
  background-color: #f9f9f9;
  border-right: 1px solid #ddd;
}

.edit-area {
  padding: 20px;
}

.medical-record {
  margin: 0 auto;
  border: 1px solid #000;
  padding: 30px;
  font-family: "SimSun", "宋体", serif;
  line-height: 1.8;
  word-wrap: break-word;
  font-size: 16px;
}

.medical-record h1 {
  text-align: center;
  font-size: 30px;
  margin-bottom: 20px;
  font-family: 'Microsoft YaHei', serif;
}

.document p {
  margin: 12px 0;
  font-size: 16px;
  font-family: "SimSun", "宋体", serif;
}

.strong {
  font-weight: bold;
  font-family: 方正小标宋简体, serif;
  font-size: 20px;
}

.medical-record .signature {
  text-align: right;
  margin-top: 30px;
  font-size: 16px;
  font-style: italic;
}

.signature {
  margin-right: 80px;
}

.pdfButton {
  margin-top: 20px;
  margin-left: 44%;
}

.divider {
  margin: 20px 0;
  border: 0;
  border-top: 1px solid #000000;
}


</style>