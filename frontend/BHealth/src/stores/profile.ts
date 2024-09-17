import {defineStore} from "pinia";

interface ProfileState {
  username: string;
  id: string;
  mobile: string;
  email: string;
  avatar: string;
  type: string;
  introduction: string;
}

export const useProfileStore = defineStore('profile', {
  state: (): ProfileState => ({
    username: '',
    id: '0',
    mobile: '',
    email: '',
    avatar: '',
    type: '',
    introduction: '',
  }),

  actions: {
    updateProfile(profile: {
      username: string;
      id: string;
      mobile: string;
      email: string;
      avatar: string;
      type: string;
      introduction: string;
    }) {
      this.username = profile.username;
      this.id = profile.id;
      this.mobile = profile.mobile;
      this.email = profile.email;
      this.avatar = profile.avatar;
      this.type = profile.type;
      this.introduction = profile.introduction;
    },
  },

  persist: {
      key : 'profile-store',
      storage: window.localStorage,
      paths: ['username', 'id', 'mobile', 'email', 'avatar', 'type', 'introduction']
  }
});