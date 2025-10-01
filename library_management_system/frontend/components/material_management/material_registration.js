const MaterialRegistration = {
    components: {
        'step1': MaterialRegistrationStep1,
        'step2': MaterialRegistrationStep2
    },
    data() {
        return {
            currentStep: 'step1',
            barcode: ''
        };
    },
    methods: {
        handleBarcodeChecked(barcode) {
            this.barcode = barcode;
            this.currentStep = 'step2';
        },
        resetToStep1() {
            this.barcode = '';
            this.currentStep = 'step1';
        }
    },
    template: `
        <div>
            <step1 v-if="currentStep === 'step1'" @barcode-checked="handleBarcodeChecked"></step1>
            <step2 v-if="currentStep === 'step2'" :barcode="barcode" 
                  @back-to-step1="resetToStep1"
                  @material-registered="resetToStep1"></step2>
        </div>
    `
};
