// axios plugin
import axios from "axios";

// base request object with baseURL and timeout
const request = axios.create({
  baseURL: "http://127.0.0.1:6969/api/",
  timeout: 5000,
});

export { request };
