<script setup lang="ts">

import DrugsGraph from "@/components/DrugsInfo/DrugsGraph.vue";
import {computed, onMounted, reactive, ref} from "vue";
import api from "@/api";
import {ElMessage} from "element-plus";
import router from "@/router";

const drugs = ref([]);
const getAllDrugs = async () => {
  const res = await api.getAllDrugs();
  drugs.value = res.results;
  console.log('drugs:', drugs.value);
  for (let i = 0; i < drugs.value.length; i++) {
    drugsName.push(drugs.value[i].name);
  }
};

onMounted(() => {
  getAllDrugs();
});

let drugsName = [];
const dialogFormVisible = ref(false);
const dialogFormVisible1 = ref(false);
const dialogFormVisible2 = ref(false);
const dialogFormVisible3 = ref(false);

const formLabelWidth = '140px'


interface Form {
  name: string, price: number, stock: number, description: string, dosage: number
}

const form: Form = reactive({
  name: '',
  price: 0,
  stock: 0,
  description: '',
  dosage: 0
})

const form1: Form = reactive({
  name: '',
  price: 0,
  stock: 0,
  description: '',
  dosage: 0
})

const submitAdd = async () => {
  console.log(form);
  if (form.price <= 0) {
    ElMessage.error('价格必须大于0');
    return;
  }
  if (form.stock <= 0) {
    ElMessage.error('数量必须大于0');
    return;
  }
  if (form.dosage <= 0) {
    ElMessage.error('每日用量必须大于0');
    return;
  }

  await api.addDrug(form);
  dialogFormVisible.value = false;
}
const clickDrugId = ref(0);
const clickDrugName = ref('');
const clickDrugStock = ref(0);
const patientId = ref(0);

const editRow = (row) => {
  console.log(row);
  dialogFormVisible1.value = true;
  clickDrugId.value = row.id;
  clickDrugName.value = row.name;
  clickDrugStock.value = row.stock;
}

const addDrugStock = async () => {
  console.log(form1);
  if (form1.stock <= 0) {
    ElMessage.error('补充数量必须大于0');
    return;
  }
  dialogFormVisible1.value = false;
  form1.stock += clickDrugStock.value;
  await api.addDrugStock(form1, clickDrugId.value.toString());
}

const useDrug = async () => {
  console.log(patientId.value);
  if (patientId.value <= 0) {
    ElMessage.error('请输入正确的病人编号');
    return;
  }
  dialogFormVisible2.value = false;
  await api.useDrug({userid : patientId.value.toString()});
}

const currentPage = ref(1);
const perPage = ref(5);
const inputPage = ref(1);

const totalPages = computed(() => Math.ceil(drugs.value.length / perPage.value));

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * perPage.value;
  const end = start + perPage.value;
  console.log('start:', drugs.value.slice(start, end));
  return drugs.value.slice(start, end);
});

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

const jumpToPage = () => {
  if (inputPage.value >= 1 && inputPage.value <= totalPages.value) {
    currentPage.value = inputPage.value;
  } else {
    inputPage.value = currentPage.value;
  }
};
const getPatient = async () => {
  dialogFormVisible3.value = false;
  router.push('/diagnosis/' + patientId.value);
}

</script>

<template>
  <div class="drugsData">
    <h1 class="drugsDataTitle">医院药品库存情况</h1>
  </div>
  <div class="drugsInfo">
  <DrugsGraph> </DrugsGraph>
  <el-dialog v-model="dialogFormVisible" title="上传新药品" width="500px" >
    <el-form :model="form">
      <el-form-item label="药品名称" :label-width="formLabelWidth">
        <el-input v-model="form.name"></el-input>
      </el-form-item>
      <el-form-item label="价格" :label-width="formLabelWidth">
        <el-input v-model="form.price" type="number"></el-input>
      </el-form-item>
      <el-form-item label="描述" :label-width="formLabelWidth">
        <el-input v-model="form.description"></el-input>
      </el-form-item>
      <el-form-item label="数量" :label-width="formLabelWidth">
        <el-input-number v-model="form.stock" :min="1" :step="1"></el-input-number>
      </el-form-item>
      <el-form-item label="每日用量" :label-width="formLabelWidth">
        <el-input-number v-model="form.dosage" :min="1" :step="1"></el-input-number>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button type="primary" @click="submitAdd">
          确认
        </el-button>
        <el-button @click="dialogFormVisible = false">取消</el-button>
      </div>
    </template>
  </el-dialog >
  <el-dialog v-model="dialogFormVisible1" title="补充药品" width="500px" >
    <el-form :model="form1">
      <el-form-item label="药品名称" :label-width="formLabelWidth">
        <el-select v-model="clickDrugName" placeholder="请选择药品">
          <el-option
            v-for="item in drugsName"
            :key="item"
            :label="item"
            :value="item"
          >
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="补充数量" :label-width="formLabelWidth">
        <el-input-number v-model="form1.stock" :min="1" :step="1"></el-input-number>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button type="primary" @click="addDrugStock">
          确认
        </el-button>
        <el-button @click="dialogFormVisible1 = false">取消</el-button>
      </div>
    </template>
  </el-dialog>
  <el-dialog v-model="dialogFormVisible2" title="为病人取药" width="500px">
    <el-form>
      <el-form-item label="病人编号" :label-width="formLabelWidth">
        <el-input-number v-model="patientId" :min="1" :step="1"></el-input-number>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button type="primary" @click="useDrug">
          确认
        </el-button>
        <el-button @click="dialogFormVisible2 = false">取消</el-button>
      </div>
    </template>
  </el-dialog>
  <el-dialog v-model="dialogFormVisible3" title="查看病人医嘱" width="500px">
    <el-form>
      <el-form-item label="病人编号" :label-width="formLabelWidth">
        <el-input-number v-model="patientId" :min="1" :step="1"></el-input-number>
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button type="primary" @click="getPatient">
          确认
        </el-button>
        <el-button @click="dialogFormVisible3 = false">取消</el-button>
      </div>
    </template>
  </el-dialog>
  <div class="addButton">
    <el-button type="primary" @click="dialogFormVisible = true" size="default">添加新药品</el-button>
    <el-button type="warning" @click="dialogFormVisible3 = true" size="default">查看病人医嘱</el-button>
    <el-button type="info" @click="dialogFormVisible2 = true" size="default">为病人取药</el-button>
  </div>
  <div class="tableContainer">
      <table>
        <thead>
          <tr>
            <th>药品编号</th>
            <th>药品名</th>
            <th>价格</th>
            <th>库存</th>
            <th>描述</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in paginatedData" :key="index">
            <td>{{ row.id }}</td>
            <td>{{ row.name }}</td>
            <td>{{ row.price }}</td>
            <td>{{ row.stock }}</td>
            <td>{{ row.description }}</td>
            <td>
              <el-button @click="editRow(row)" type="success" size="small">补充药品</el-button>
            </td>
          </tr>
        </tbody>
      </table>
  </div>
  <div class="pagination">
      <el-button @click="prevPage" :disabled="currentPage === 1" type="primary">上一页</el-button>
      <span class="pageNumber">{{ currentPage }} / {{ totalPages }} 页</span>
      <el-button @click="nextPage" :disabled="currentPage === totalPages" type="primary">下一页</el-button>
      <span class="pageNumber">跳至</span>
      <el-input type="number" v-model="inputPage" @keyup.enter="jumpToPage" style="width: 60px;"></el-input>
      <span class="pageNumber">页</span>
  </div>
  </div>
</template>

<style scoped>
.drugsInfo {
  width: 1350px;
  margin: 0 auto 5%;
}
.drugsData {
  margin-top: 5%;
}

.drugsDataTitle {
  font-size: 30px;
  text-align: center;
}

.tableContainer {
  margin: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

thead {
  background-color: #f4f4f4;

  font-weight: bold;
}

tbody {
  font-family: 'Microsoft YaHei', serif;
}

th {
  background-color: #f4f4f4;
}

tr:nth-child(odd) {
  background-color: #f9f9f9; /* 斑马纹样式 */
}

tr:hover {
  background-color: #f1f1f1; /* 鼠标悬停效果 */
}

.pagination {
  text-align: center;
  margin-top: 2%;
  margin-left: 70%;
}

button {
  padding: 5px 10px;
}

.pageNumber {
  margin-left: 10px;
  margin-right: 10px;
}

.el-button {
  margin-right: 5px;
}

.addButton {
  margin-left: 75%;
}

.drugsDataTitle {
  font-size: 2.5rem; /* 字体大小 */
  color: #007BFF; /* 天蓝色 */
  text-align: center; /* 居中对齐 */
  padding: 20px 0; /* 上下内边距 */
  margin-bottom: 20px; /* 底部外边距 */
  background-color: rgba(135, 206, 250, 0.7); /* 半透明天蓝色背景 */
  border-radius: 10px; /* 圆角边框 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 添加阴影效果 */
  text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.8); /* 字体阴影 */
  display: flex; /* 使用 flexbox 布局 */
  justify-content: center; /* 水平居中对齐 */
  align-items: center; /* 垂直居中对齐 */
  transition: transform 0.3s ease, background-color 0.3s ease; /* 动画过渡 */
}

.drugsDataTitle::after {
  content: "💊"; /* 药品图标 */
  display: inline-block;
  font-size: 1.5rem; /* 图标大小 */
  margin-left: 10px; /* 与标题之间的间距 */
  animation: bounce 1s infinite; /* 动画效果 */
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}

::v-deep .el-dialog {
  margin-top: 13%;
}

::v-deep .el-dialog__title {
  font-family: 'Helvetica Neue', Arial, sans-serif;
  font-size: 20px;
  color: #333;
  font-weight: bold;
}


::v-deep .el-dialog {
  border-radius: 30px; /* 圆角 */
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15); /* 增加阴影 */
  padding: 30px;
  background-color: #f7f7f7;
}

::v-deep .el-dialog__body {
  font-family: 'Arial', sans-serif;
  font-size: 16px;
  color: #333;
  padding: 20px;
  line-height: 1.6;
}

::v-deep .el-dialog__footer {
  padding: 15px;
  text-align: right;
  background-color: #f0f0f0;
  border-bottom-left-radius: 30px; /* 底部圆角 */
  border-bottom-right-radius: 30px; /* 底部圆角 */
}

::v-deep .el-dialog__header {
  font-family: 'Arial', sans-serif;
  font-size: 20px;
  font-weight: bold;
  background-color: #f0f0f0;
  color: white; /* 标题文字颜色 */
  padding: 15px;
  border-top-left-radius: 30px; /* 顶部圆角 */
  border-top-right-radius: 30px; /* 顶部圆角 */
  text-align: center;

}

</style>