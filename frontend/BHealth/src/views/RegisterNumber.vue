<template>
  <div>
    <div class="main">
    <div class="navigate">
      <div class="selectDepartment">
        <el-select v-model="department" placeholder="请选择" style="width: 120px;">
          <el-option
            v-for="item in allDepartment"
            :key="item"
            :label="item"
            :value="item"
          >
          </el-option>
        </el-select>
      </div>
      <div class="searchDiv">
          <el-input v-model="searchValue" placeholder="请输入姓名" @keyup.enter="searchByName">
              <template #prepend>
                  <div class="search-icon-container">
                      <el-icon size="20px">
                          <Search/>
                      </el-icon>
                  </div>
              </template>
          </el-input>
          <div>
              <el-button type="primary" @click="searchByName">搜索</el-button>
          </div>
      </div>
<!--      <div class="createDoctor">-->
<!--        <el-button type="info" @click="createDoctor">新增医生</el-button>-->
<!--      </div>-->
    </div>
    <div class="tableContainer">
      <table>
        <thead>
          <tr>
            <th>序号</th>
            <th>医生姓名</th>
            <th>学历</th>
            <th>开始工作时间</th>
            <th>毕业学校</th>
            <th>职称</th>
            <th>科室</th>
            <th>介绍</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in paginatedData" :key="index">
            <td>{{ index + 1 }}</td>
            <td>{{ row.name }}</td>
            <td>{{ row.education }}</td>
            <td>{{ row.workTime }}</td>
            <td>{{ row.school }}</td>
            <td>{{ row.title }}</td>
            <td>{{ row.department }}</td>
            <td>{{ row.introduction }}</td>
            <td>
              <el-button @click="editRow(row)" type="success" size="small">放号</el-button>
              <el-button @click="deleteRow(row)" type="danger" size="small">删除</el-button>
              <el-button type="primary" @click="register(row)" size="small">挂号</el-button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="pagination">
      <el-button @click="prevPage" :disabled="currentPage === 1" type="primary">上一页</el-button>
      <span class="pageNumber">{{ currentPage }} / {{ totalPages }} 页</span>
      <el-button @click="nextPage" :disabled="currentPage === totalPages" type="primary">下一页</el-button>
      <!-- 添加跳至多少页的输入框 -->
      <span class="pageNumber">跳至</span>
      <el-input type="number" v-model="inputPage" @keyup.enter="jumpToPage" style="width: 60px;"></el-input>
      <span class="pageNumber">页</span>
    </div>
  </div>
  <el-dialog v-model="dialogFormVisible" title="医生放号" width="500px" >
    <el-form :model="form">
      <el-form-item label="放号数量" :label-width="formLabelWidth" >
        <el-input v-model="form.count" autocomplete="off" placeholder="请输入" type="number"/>
      </el-form-item>
      <el-form-item label="放号时间" :label-width="formLabelWidth">
        <el-time-select
          v-model="form.startTime"
          start="08:30"
          step="00:30"
          end="18:30"
          placeholder="请选择放号时间段"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button type="primary" @click="submitNumber">
          确认
        </el-button>
        <el-button @click="dialogFormVisible = false">取消</el-button>
      </div>
    </template>
  </el-dialog >
  <el-dialog v-model="dialogFormVisible1" title="挂号" width="500px">
    <el-form :model="registerData">
      <el-form-item label="预约时间" :label-width="formLabelWidth">
        <el-time-select
          v-model="registerData.doctorStartTime"
          start="08:30"
          step="00:30"
          end="18:30"
          placeholder="请选择放号时间段"
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button type="primary" @click="submitRegister">
          确认
        </el-button>
        <el-button @click="dialogFormVisible1 = false">取消</el-button>
      </div>
    </template>
  </el-dialog>
  <el-dialog v-model="dialogFormVisible2" title="请先填写您的症状" width="500px">
<!--    填写症状描述-->
  <el-input
    type="textarea"
    v-model="description"
    placeholder="请输入症状描述"
    size="large"
    class="inputDescription"
  />

  <template #footer>
    <div class="dialog-footer">
      <el-button type="primary" @click="submitDescription">
        查询
      </el-button>
      <el-button @click="dialogFormVisible2 = false">取消</el-button>
    </div>
  </template>

</el-dialog>
<el-dialog v-model="dialogFormVisible3" title="我们的ai生成推荐结果是" width="500px">
   <span class="aiAnswer">{{aiAnswer}}</span>
</el-dialog>
  </div>
  <div class="ai" @click="openAi">
    <p class="aip">AI</p>
    <div class="ai-img">
      <el-image
        style="margin-top: 20px"
        src="src/assets/ai.png"
        fit="cover"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref, computed, reactive} from 'vue';
import { Search } from '@element-plus/icons'
import {ElLoading, ElMessage} from "element-plus";

const searchValue = ref('');
const department = ref('全部');
const currentPage = ref(1);
const perPage = ref(10); // 每页显示的行数
const inputPage = ref(1); // 输入跳转页码的绑定值
const tableData = ref([
  {name : '张三', education : '本科', workTime : '2010-09-01', school : '清华大学', title : '主任医师', department : '内科', introduction : '擅长治疗感冒'},
  {name : '李四', education : '硕士', workTime : '2012-09-01', school : '北京大学', title : '副主任医师', department : '外科', introduction : '擅长治疗骨折'},
  {name : '王五', education : '博士', workTime : '2015-09-01', school : '复旦大学', title : '主治医师', department : '妇产科', introduction : '擅长治疗妇科疾病'},
  {name : '赵六', education : '本科', workTime : '2018-09-01', school : '上海交通大学', title : '住院医师', department : '儿科', introduction : '擅长治疗儿童感冒'},
  {name : '钱七', education : '硕士', workTime : '2020-09-01', school : '南京大学', title : '主任医师', department : '皮肤科', introduction : '擅长治疗皮肤病'},
  {name : '孙八', education : '博士', workTime : '2021-09-01', school : '浙江大学', title : '主治医师', department : '耳鼻喉科', introduction : '擅长治疗耳鼻喉疾病'},
  {name : '周九', education : '本科', workTime : '2019-09-01', school : '武汉大学', title : '住院医师', department : '口腔科', introduction : '擅长治疗口腔疾病'},
  {name : '吴十', education : '硕士', workTime : '2017-09-01', school : '中山大学', title : '主任医师', department : '骨科', introduction : '擅长治疗骨折'},
  {name : '郑十一', education : '博士', workTime : '2016-09-01', school : '华中科技大学', title : '主治医师', department : '神经科', introduction : '擅长治疗神经疾病'},
  {name : '马十二', education : '本科', workTime : '2014-09-01', school : '华南理工大学', title : '住院医师', department : '心血管科', introduction : '擅长治疗心血管疾病'},
  {name : '陈十三', education : '硕士', workTime : '2013-09-01', school : '四川大学', title : '主任医师', department : '肿瘤科', introduction : '擅长治疗肿瘤'},
  {name : '林十四', education : '博士', workTime : '2011-09-01', school : '西安交通大学', title : '主治医师', department : '消化科', introduction : '擅长治疗消化系统疾病'},
]);
const allDepartment = ref(['全部', '内科', '外科', '妇产科', '儿科', '皮肤科','耳鼻喉科','口腔科','骨科','神经科','心血管科','肿瘤科','消化科']);
const dialogFormVisible = ref(false);
const dialogFormVisible1 = ref(false);
const dialogFormVisible2 = ref(false);
const dialogFormVisible3 = ref(false);
const canRegister = ref(false);
const description = ref('');
const formLabelWidth = '140px'
// 计算总页数
const totalPages = computed(() => Math.ceil(tableData.value.length / perPage.value));
const form = reactive({
  count: 0,
  startTime: '',
})
const registerData = reactive({
  doctorDepartment: '',
  doctorName: '',
  doctorId: '',
  doctorStartTime: '',
})
// 计算当前页的数据
const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * perPage.value;
  const end = start + perPage.value;
  return tableData.value.slice(start, end);
});

// 下一页
const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

// 上一页
const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

// 跳转到指定页
const jumpToPage = () => {
  if (inputPage.value >= 1 && inputPage.value <= totalPages.value) {
    currentPage.value = inputPage.value;
  } else {
    inputPage.value = currentPage.value;
  }
};

const editRow = (row) => {
  console.log('放号', row);
  dialogFormVisible.value = true;
};

const deleteRow = (row) => {
  // 删除当前行
  tableData.value = tableData.value.filter(item => item !== row);
  if (tableData.value.length % perPage.value === 0 && currentPage.value > 1) {
    currentPage.value--;
  }
  console.log('删除', row);
  ElMessage.success('删除成功');
};

const searchByName = () => {
  console.log('搜索', searchValue.value);
};

const submitNumber = () => {
  console.log('提交', form);
  dialogFormVisible.value = false;
  ElMessage.success('放号成功');
};

const register = (row) => {
  console.log('挂号', row);
  dialogFormVisible1.value = true;
  //传入拿到剩余人数,是否可以挂号
  //TODO
};

const submitRegister = () => {
  console.log('提交挂号');
  dialogFormVisible1.value = false;
  if (canRegister.value) {
    ElMessage.success('挂号成功');
  } else {
    ElMessage.error('挂号失败: 该医生无空闲号源');
  }
};

const aiAnswer = ref('111');
const submitDescription = () => {
  //提交Description
  console.log('提交症状描述', description.value);
  const loading = ElLoading.service({
    lock: true,
    text: 'Loading',
    background: 'rgba(0, 0, 0, 0.7)',
  })
  setTimeout(() => {
    loading.close();
    dialogFormVisible2.value = false;
    dialogFormVisible3.value = true;
    description.value='';
  }, 3000)
}

// const createDoctor = () => {
//   console.log('新增医生');
//   //跳转到新增医生页面
//   //TODO
// };

const openAi = () => {
  console.log('打开AI聊天');
  dialogFormVisible2.value = true;
};

</script>

<style>
.main {
    width: 1350px;
    margin: auto;
    margin-top: 64px;
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

.el-button--success {
  background-color: #28a745;
  border-color: #28a745;
  color: #fff;
}

.el-button--danger {
  background-color: #dc3545;
  border-color: #dc3545;
  color: #fff;
}

.search-icon-container {
    width: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.searchDiv {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-left: 20px;
    width: 500px;
}

.navigate {
    display: flex;
    justify-content: flex-start;
    margin: 20px;
}

.selectDepartment {
    display: flex;
    align-items: center;
    gap: 10px;
}

.dialog-footer {
  display: flex;
  justify-content: center;
  align-items: center;
}

.el-form {
  margin-right: 55px;
  margin-top: 20px;
}

.el-dialog {
  margin-top: 13%;
}

.createDoctor {
  margin-left: 50%;
}

.ai {
  position: fixed;
  right: 5%;
  bottom: 3%;
  width: 60px;
  height: 60px;
  background-color: #8c8ddc;
  z-index: 1000;
  border-radius: 25%;
  cursor: pointer;
  border: thin solid #5153d5;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.ai:hover {
  background-color: #7c7cbf;
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
  transform: scale(1.1);
}

.ai:active {
  transform: scale(1.05);
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(124, 124, 191, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(124, 124, 191, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(124, 124, 191, 0);
  }
}

.ai:hover {
  animation: pulse 1.5s infinite;
}

.ai-img {
  display: flex;
  justify-content: center;
  align-items: center;
  max-height: 20px;
  max-width: 30px;
  z-index: 1001;
  margin-left: 14px;
}

.aip {
  text-align: center;
  font-size: 16px;
  font-family: "幼圆", sans-serif;
  margin-top: 10px;
  color: #ffffff; /* Solid white color for better contrast */
  font-weight: bold; /* Make the text stand out more */
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); /* Adds a subtle shadow to make the white text more readable */
  transition: all 0.3s ease;
}

.el-dialog__title {
  font-family: 'Helvetica Neue', Arial, sans-serif;
  font-size: 20px;
  color: #333;
  font-weight: bold;
}

.aiAnswer {
  font-family: 'Courier New', Courier, monospace;
  font-size: 24px;
  color: #007BFF;
  font-weight: 600;
  display: block;
  text-align: center;
  margin-top: 20px;
}

.el-dialog {
  border-radius: 30px; /* 圆角 */
  box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.15); /* 增加阴影 */
  padding: 30px;
  background-color: #f7f7f7;
}

.el-dialog__body {
  font-family: 'Arial', sans-serif;
  font-size: 16px;
  color: #333;
  padding: 20px;
  line-height: 1.6;
}

.el-dialog__footer {
  padding: 15px;
  text-align: right;
  background-color: #f0f0f0;
  border-bottom-left-radius: 30px; /* 底部圆角 */
  border-bottom-right-radius: 30px; /* 底部圆角 */
}

.el-dialog__header {
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
