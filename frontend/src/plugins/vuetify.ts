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
        primary: '#263238',
        secondary: '#455A64',
        accent: '#37474F',
        error: '#b71c1c'
    }
});