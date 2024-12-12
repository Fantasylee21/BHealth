<template>
  <div class="wangEditor">
    <div class="editor-container">
      <Toolbar class="toolbar" :editor="editorRef" :defaultConfig="toolbarConfig" mode="default" />
      <Editor class="editor" v-model="valueHtml" :defaultConfig="editorConfig" mode="default" @onCreated="handleCreated" @customPaste="customPaste" />
      <el-button class="submit-button" @click="getEditorHTML">提交</el-button>
    </div>
  </div>
</template>

<script setup>
import '@wangeditor/editor/dist/css/style.css';
import { onBeforeUnmount, ref, shallowRef } from 'vue';
import { Editor, Toolbar } from '@wangeditor/editor-for-vue';
import {ElLoading} from "element-plus";

const editorRef = shallowRef();
const valueHtml = ref('<p>发布一则BHealth的新闻吧！！！</p>');
const toolbarConfig = {};
const editorConfig = ref({ placeholder: '请输入内容...', MENU_CONF: {} });

// 自定义图片上传
editorConfig.value.MENU_CONF['uploadImage'] = {
  async customUpload(file, insertFn) {
    const base64 = URL.createObjectURL(file);
    insertFn(base64, 'img');
  },
};

// 自定义视频上传
editorConfig.value.MENU_CONF['uploadVideo'] = {
  async customUpload(file, insertFn) {
    const base64 = URL.createObjectURL(file);
    insertFn(base64, 'video');
  },
};

const handleCreated = editor => {
  editorRef.value = editor;
};

const customPaste = (editor, event, callback) => {
  const text = event.clipboardData.getData('text/plain');
  if (text) {
    editor.insertText(text);
    event.preventDefault();
    callback(false);
  }
};

const emit = defineEmits(['getEditorHTML']);
const getEditorHTML = () => {
  const loading = ElLoading.service({
    lock: true,
    text: '跳转中',
    background: 'rgba(0, 0, 0, 0.7)',
  })
  setTimeout(() => {
    loading.close();
  }, 300);
//   时间到后才会执行这个函数

  emit('getEditorHTML', valueHtml.value);
};

onBeforeUnmount(() => {
  const editor = editorRef.value;
  if (editor) editor.destroy();
});
</script>

<style scoped>
.editor-container {
  border: 1px solid #ccc;
  width: 100%;
  margin: auto;
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  background-color: #f9f9f9;
  padding: 20px;
  z-index: 2000;
}


.toolbar {
  border-bottom: 1px solid #ccc;
}

.editor {
  min-height: 300px;
  margin-top: 20px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #fff;
}

.submit-button {
  margin: 20px auto;
  display: block;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 10px 20px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #0056b3;
}

</style>
