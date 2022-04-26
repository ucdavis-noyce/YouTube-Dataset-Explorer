const app = new Vue({

    el: '#app',

    data: {
        ideologies: ['Left', 'Center-left', 'Center', 'Center-right', 'Right'],
        selectedIdeology: null,
        selectedPuppetId: null,
        loading: false,
        numSockPuppets: null,
        puppetId: null,
        puppetData: null,
        panel: null,
        hideUnks: false
    },

    methods: {

        setIdeology: async function (ideology) {
            this.selectedIdeology = ideology;
            this.selectedPuppetId = null;
            this.puppetId = null;
            this.puppetData = null;
            this.numSockPuppets = await getNumSockPuppets(ideology);
        },

        downloadPuppet: async function () {
            var blob = new Blob([JSON.stringify(this.puppetData)], {type: "application/json;charset=utf-8"});
            saveAs(blob, `${this.selectedIdeology}-${this.selectedPuppetId}.json`);
        },

        loadPuppet: async function (puppetId) {
            this.selectedPuppetId = puppetId;
            this.puppetData = Object.freeze(await getSockPuppet(this.selectedIdeology, puppetId));
        },

        loadRandom: async function () {
            const _id = Math.floor(Math.random() * this.numSockPuppets);
            this.puppetId = _id;
            this.loadPuppet(_id);
        }

    },

    computed: {
        numSockPuppetsPrompt: function () {
            if (this.numSockPuppets) {
                return 'Total # of sock puppets: ' + this.numSockPuppets;
            }
            return ' ';
        },

        trainingData: function () {
            if (this.puppetData) {
                return this.puppetData.args.training.split(',');
            }
            return [];
        },

        homepageData: function () {
            let training_end = false;
            
            if (!this.puppetData) {
                return [];
            }

            for (const action of this.puppetData.actions) {

                if (action.action == 'training_end') {
                    training_end = true;
                }

                if (!training_end) {
                    continue;
                }

                if (action.action == 'get_homepage') {
                    return action.params;
                }

            }
        },



        testingData: function () {
            let testing_start = false;

            const recommendations = [
                [this.puppetData.args.testSeed]
            ];

            for (const action of this.puppetData.actions) {

                if (action.action == 'testing_start') {
                    testing_start = true;
                }

                if (!testing_start) {
                    continue;
                }

                if (action.action == 'get_recommendations') {
                    recommendations.push(action.params);
                }

            }

            return recommendations;
        }

    }

});