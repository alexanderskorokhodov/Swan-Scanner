import axios from "axios";

class Service{

    async sendImage(id, file_path) {
        console.log(file_path)
      return await axios
			.post("http://localhost:8000/imageservice/", {
				image_id:id,
				src:file_path
			})
    }

    async load_data(){
      return axios.get("http://localhost:8000/imageservice/")
    }


  
    async deleteImage(id){
      await axios
		   .post("http://localhost:8000/deleteimage/", {
				image_id:id
			})
    }

    async highlightImage(id){
      await axios
		   .post("http://localhost:8000/highlightimage/", {
				image_id:id
			})
    }
    async rewriteNote(id, note){
      await axios
		   .post("http://localhost:8000/rewritenote/", {
				image_id:id,
        note:note
			})
    }

}

export default Service;