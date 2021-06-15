const app = Vue.createApp({
    data () {
        return {
            firstname: "Frank",
            lastname: "Yanfeng",
            email: "fanyank@outlook.com",
            gender: "male",
            picture: "https://randomuser.me/api/portraits/men/10.jpg"
        }
    },
    methods: {
        async getUser() {
            const res = await fetch('https://randomuser.me/api');
            const { results } = await res.json();

            // console.log(results);
            user = results[0];
            this.firstname = user.name.first;
            this.lastname = user.name.last;
            this.email = user.email;
            this.picture = user.picture.large;
            this.gender = user.gender;
        }
    }
});

app.mount('#app');