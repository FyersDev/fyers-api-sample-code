class ErrorHandler {
    #genricErrorStructure = {s: 'error', code: 500, message: 'Genric Error'}


    constructor(errorObject) {
        this.errorObject = errorObject
    }

    getError() {
        if (this.errorObject && this.errorObject.response && this.errorObject.response.data) {
            return this.errorObject.response.data;
        } else if (this.errorObject && (this.errorObject.code === 'ENOTFOUND')) {
            return this.setError(this.errorObject.errno, this.errorObject.code)
        }else if(this.errorObject.code){
            return this.setError(null, this.errorObject.code)
        } else if(this.errorObject){
            return this.setError(null, this.errorObject)
        } {
            return this.#genricErrorStructure
        }
    }


    setError(code, message) {
        if(code){
            this.#genricErrorStructure.code = code
        }
        if(message){
            this.#genricErrorStructure.message = message
        }

        return this.#genricErrorStructure
    }

}

module.exports = ErrorHandler;