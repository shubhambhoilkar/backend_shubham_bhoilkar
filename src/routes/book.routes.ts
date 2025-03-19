import express from "express";
import { createBook, getBooks } from "../controllers/book.controller";
import upload from "../middleware/multer.middleware";

const router = express.Router();
router.post("/", upload.single("coverImage"), createBook);
router.get("/", getBooks);

export default router;
