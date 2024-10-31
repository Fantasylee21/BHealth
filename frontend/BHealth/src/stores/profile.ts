import { defineStore } from "pinia";

interface ProfileState {
  id: number;
  username: string;
  email: string;
  avatar: string | null;
  type: string;
  introduction: string | null;
  title: string;
  category: string;
  education: string;
  school: string;
  work_time: string;
  is_active: boolean;
  is_superuser: boolean;
  is_staff: boolean;
  date_joined: string;
  create_time: string;
  update_time: string;
}

export const useProfileStore = defineStore('profile', {
  state: (): ProfileState => ({
    id: 0,
    username: '',
    email: '',
    avatar: null,
    type: '',
    introduction: null,
    title: '',
    category: '',
    education: '',
    school: '',
    work_time: '',
    is_active: true,
    is_superuser: false,
    is_staff: false,
    date_joined: '',
    create_time: '',
    update_time: '',
  }),

  actions: {
    updateProfile(profile: ProfileState) {
      this.id = profile.id;
      this.username = profile.username;
      this.email = profile.email;
      this.avatar = profile.avatar;
      this.type = profile.type;
      this.introduction = profile.introduction;
      this.title = profile.title;
      this.category = profile.category;
      this.education = profile.education;
      this.school = profile.school;
      this.work_time = profile.work_time;
      this.is_active = profile.is_active;
      this.is_superuser = profile.is_superuser;
      this.is_staff = profile.is_staff;
      this.date_joined = profile.date_joined;
      this.create_time = profile.create_time;
      this.update_time = profile.update_time;
    },
  },

  persist: {
    key: 'profile-store',
    storage: window.localStorage,
    paths: [
      'id', 'username', 'email', 'avatar', 'type', 'introduction', 'title',
      'category', 'education', 'school', 'work_time', 'is_active', 'is_superuser',
      'is_staff', 'date_joined', 'create_time', 'update_time'
    ]
  },
});
