// axios plugin
import axios from "axios";

// base request object with baseURL and timeout
const request = axios.create({
  baseURL: "/api",
  timeout: 25000,
});

export { request };
