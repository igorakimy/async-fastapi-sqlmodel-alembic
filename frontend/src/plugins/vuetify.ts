import Vue from 'vue';
import Vuetify from 'vuetify';
import VeeValidate, { Validator } from 'vee-validate';
import ru from '@/locale/ru';


Validator.localize({'ru': ru});

Vue.use(VeeValidate, {
    locale: 'ru'
});


Vue.use(Vuetify, {
    iconfont: 'md',
    theme: {
      primary: '#1976D2',
      secondary: '#424242',
      accent: '#82B1FF',
      error: '#FF5252',
      info: '#2196F3',
      success: '#4CAF50',
      warning: '#FFC107'
    }
});