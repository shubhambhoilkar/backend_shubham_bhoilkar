import { Request, Response } from "express";
import prisma from "../models/prisma";

export const createBook = async (req: Request, res: Response) => {
  const { title, author } = req.body;
  const coverImage = req.file ? `/uploads/${req.file.filename}` : null;
  const book = await prisma.book.create({ data: { title, author, coverImage } });
  res.json(book);
};

export const getBooks = async (req: Request, res: Response) => {
  const { page = 1, limit = 10, search = "" } = req.query;
  const books = await prisma.book.findMany({
    where: { title: { contains: search as string, mode: "insensitive" } },
    skip: (+page - 1) * +limit,
    take: +limit,
  });
  res.json(books);
};
