<script setup lang="ts">

</script>

<template>
  <div id="app" class="user-profile">
    <h1>开具医嘱</h1>
    <form @submit.prevent="submitPrescription">
      <div class="form-group">
        <h3>医嘱内容</h3>
        <textarea id="content" v-model="prescription.content" required></textarea>
      </div>
      <div class="form-group">
        <h3>药品清单</h3>
        <div v-for="(drug, index) in prescription.takenDrugs" :key="index" class="drug-item">
          <input
              v-model="drug[0]"
              placeholder="药品名称"
              required
          />
          <input
              type="number"
              v-model="drug[1]"
              placeholder="数量"
              required
              min="1"
          />
          <button type="button" @click="removeDrug(index)">删除</button>
        </div>
        <button type="button" @click="addDrug" class="add-drug-button">添加药品</button>
      </div>
      <button type="submit" class="submit-button">提交医嘱</button>
    </form>
    <div v-if="submitted" class="submitted-prescription">
      <h2>提交的医嘱:</h2>
      <pre>{{ formattedPrescription }}</pre>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';

const prescription = reactive({
  content: '',
  takenDrugs: [['', 1]], // 初始化一个药品
});
const submitted = ref(false);

const addDrug = () => {
  prescription.takenDrugs.push(['', 1]);
};

const removeDrug = (index) => {
  prescription.takenDrugs.splice(index, 1);
};

const submitPrescription = () => {
  submitted.value = true;
};

const formattedPrescription = () => {
  return JSON.stringify({ content: { content: prescription.content, takenDrugs: prescription.takenDrugs } }, null, 2);
};
</script>

<style scoped>
.user-profile {
  width: 900px;
  padding: 200px;
  margin: 0 auto;
  background-color: #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-radius: 16px;
  font-family: Arial, sans-serif;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

textarea {
  width: 100%;
  height: 100px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: none;
}

.drug-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

input {
  flex: 1;
  margin-right: 10px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  background-color: #007BFF;
  color: white;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.add-drug-button {
  margin-top: 10px;
}

.submit-button {
  background-color: #28A745;
}

.submit-button:hover {
  background-color: #218838;
}

.submitted-prescription {
  margin-top: 20px;
  background: #f8f9fa;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>

