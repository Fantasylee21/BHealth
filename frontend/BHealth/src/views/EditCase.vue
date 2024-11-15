<template>
  <div class="editCase">
    <el-container>
      <el-row>
        <!-- Left Display Area -->
        <el-col :span="12" class="display-area">
          <div class="medical-record" ref="displayContent">
            <h1>计算机学院BHealth医院</h1>
            <div class="document">
              <!-- Name, Gender, Age on the same line -->
              <div class="patient-info">
                <p><strong>姓名：</strong>{{ patientInfo.name }}</p>
                <p><strong>性别：</strong>{{ patientInfo.gender }}</p>
                <p><strong>年龄：</strong>{{ patientInfo.age }}</p>
                <p><strong>就诊科室：</strong>{{ patientInfo.department }}</p>
              </div>
              <!-- Horizontal line with spacing -->
              <hr class="divider" />
              <p><strong>就诊号：</strong>{{ patientInfo.recordNumber }}</p>
              <p><strong>就诊时间：</strong>{{ patientInfo.visitTime }}</p>
              <p><strong>联系电话：</strong>{{ patientInfo.phone }}</p>
              <p><strong>家庭住址：</strong>{{ patientInfo.address }}</p>
              <p><strong>主诉：</strong>{{ patientInfo.complaint }}</p>
              <p><strong>现病史：</strong>{{ patientInfo.currentHistory }}</p>
              <p><strong>既往史：</strong>{{ patientInfo.medicalHistory }}</p>
              <p><strong>过敏史：</strong>{{ patientInfo.allergyHistory }}</p>
              <p><strong>诊断：</strong>{{ patientInfo.diagnosis }}</p>
              <p><strong>处方：</strong>{{ patientInfo.content }}</p>
              <p><strong>药品：</strong>
                <ul>
                  <li v-for="(drug, index) in patientInfo.takenDrugs" :key="index">
                    药品:{{ drug.name }}, 每日用量:{{ drug.count }}
                  </li>
                </ul>
              </p>
              <p><strong>建议：</strong>{{ patientInfo.advice }}</p>
            </div>
            <div class="signature">
              医师签字：贾连荣 &nbsp;手签：
            </div>
          </div>
        </el-col>

        <!-- Right Edit Area -->
        <el-col :span="12" class="edit-area">
          <el-form :model="patientInfo" label-width="100px">
            <el-form-item label="姓名">
              <el-input v-model="patientInfo.name" />
            </el-form-item>
            <el-form-item label="性别">
              <el-select v-model="patientInfo.gender">
                <el-option label="男" value="男"></el-option>
                <el-option label="女" value="女"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="年龄">
              <el-input v-model="patientInfo.age" type="number" />
            </el-form-item>
            <el-form-item label="就诊科室">
              <el-input v-model="patientInfo.department" />
            </el-form-item>
            <el-form-item label="就诊号">
              <el-input v-model="patientInfo.recordNumber" />
            </el-form-item>
            <el-form-item label="就诊时间">
              <el-input v-model="patientInfo.visitTime" />
            </el-form-item>
            <el-form-item label="联系电话">
              <el-input v-model="patientInfo.phone" />
            </el-form-item>
            <el-form-item label="家庭住址">
              <el-input v-model="patientInfo.address" />
            </el-form-item>
            <el-form-item label="主诉">
              <el-input v-model="patientInfo.complaint" />
            </el-form-item>
            <el-form-item label="现病史">
              <el-input v-model="patientInfo.currentHistory" />
            </el-form-item>
            <el-form-item label="既往史">
              <el-input v-model="patientInfo.medicalHistory" />
            </el-form-item>
            <el-form-item label="过敏史">
              <el-input v-model="patientInfo.allergyHistory" />
            </el-form-item>
            <el-form-item label="诊断">
              <el-input v-model="patientInfo.diagnosis" />
            </el-form-item>
            <el-form-item label="处方">
              <el-input v-model="patientInfo.content" />
            </el-form-item>
            <el-form-item label="药品">
              <transition-group name="list" tag="div">
                <div v-for="(drug, index) in patientInfo.takenDrugs" :key="index" class="drug-item">
                  <el-row gutter={20}>
                    <el-col :span="8">
                      <el-input v-model="drug.name" placeholder="药品名称" />
                    </el-col>
                    <el-col :span="8">
                      <el-input v-model="drug.count" placeholder="用量" />
                    </el-col>
                    <el-col :span="4">
                      <el-icon @click="delDrug(index)" class="drug-action-icon" title="删除药品"><Minus /></el-icon>
                    </el-col>
                  </el-row>
                </div>
              </transition-group>
              <el-icon @click="addDrug" class="drug-action-icon add-icon" title="添加药品"><Plus /></el-icon>
            </el-form-item>
            <el-form-item label="建议">
              <el-input v-model="patientInfo.advice" />
            </el-form-item>
          </el-form>
          <el-button type="primary" @click="exportToPDF" class="pdfButton">导出为 PDF</el-button>
        </el-col>
      </el-row>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import html2pdf from 'html2pdf.js';
import { Minus, Plus} from "@element-plus/icons";

interface medicalRecord {
  name: string;
  count: string;
}

interface PatientInfo {
  content: string;
  takenDrugs: medicalRecord[];
  name: string;
  gender: string;
  age: number;
  department: string;
  recordNumber: string;
  visitTime: string;
  phone: string;
  address: string;
  complaint: string;
  currentHistory: string;
  medicalHistory: string;
  allergyHistory: string;
  diagnosis: string;
  advice: string;
}

const patientInfo = ref<PatientInfo>({
  content: '\'黄葵胶囊每粒装0.43g（相当于饮片2g）共15盒 口服 3次/日 一次5.0粒\',\n' +
    '    \'叶酸片0.4mg 共1盒 口服 1次/日 一次2.0片\',\n' +
    '    \'坎地沙坦酯片8mg 共4盒 口服 1次/日 一次8.0mg\'',
  takenDrugs: [{ name: '药品1', count: '1' }],
  name: '蔡志军',
  gender: '男',
  age: 45,
  department: '风湿免疫科',
  recordNumber: 'M207882405098',
  visitTime: '2024-05-09 14:21:52',
  phone: '13920631008',
  address: '地址',
  complaint: '腰疼，高血压，叶酸缺乏三年',
  currentHistory: '1、高血压 2、叶酸缺乏症 3、腰痛',
  medicalHistory: '既往史',
  allergyHistory: '过敏史',
  diagnosis: '1、高血压 2、叶酸缺乏症 3、腰痛',
  advice: '在用药过程中有任何身体不适，请及时前往实体医院就诊'
});

const displayContent = ref(null);

const exportToPDF = () => {
  html2pdf().from(displayContent.value).save('病例信息.pdf');
};

// Method to add a new drug input
const addDrug = () => {
  patientInfo.value.takenDrugs.push({ name: '', count: '' });
};
const delDrug = () => {
  if (patientInfo.value.takenDrugs.length === 1) {
    return;
  }
  patientInfo.value.takenDrugs.pop();
};

</script>

<style scoped>
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
  padding: 20px;
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
  margin-top: 40px;
  margin-left: 50%;
}

.drugAdd {
  cursor: pointer;
  margin-left: 20px;
}

.drugAdd .drugSub :hover {
  background-color: #f9f9f9;
}

.patient-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.patient-info p {
  margin: 0;
  padding-right: 20px; /* Add space between fields */
}

/* Styling for the horizontal line */
.divider {
  margin: 20px 0;
  border: 0;
  border-top: 1px solid #000000;
}

.drug-item {
  opacity: 1;
  transition: all 0.5s ease;
}

.list-enter-active, .list-leave-active {
  transition: all 0.5s;
}
.list-enter, .list-leave-to /* .list-leave-active in <2.1.8 */ {
  opacity: 0;
  transform: translateY(30px);
}

.drug-action-icon {
  cursor: pointer;
  color: #409eff;
  font-size: 18px;
  transition: transform 0.3s ease, color 0.3s ease;
}


.add-icon:hover {
  transform: scale(1.2) rotate(45deg);
}

</style>