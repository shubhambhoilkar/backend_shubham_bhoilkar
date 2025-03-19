import { Request, Response } from "express";
import prisma from "../models/prisma";

export const rentBook = async (req: Request, res: Response) => {
  const { userId, bookId } = req.body;

  const existingRental = await prisma.rental.findFirst({ where: { userId, returnedAt: null } });
  if (existingRental) return res.status(400).json({ error: "User already rented a book" });

  const book = await prisma.book.findUnique({ where: { id: bookId } });
  if (!book || book.isRented) return res.status(400).json({ error: "Book not available" });

  await prisma.book.update({ where: { id: bookId }, data: { isRented: true } });
  const rental = await prisma.rental.create({ data: { userId, bookId } });

  res.json(rental);
};

export const returnBook = async (req: Request, res: Response) => {
  const { rentalId } = req.body;
  const rental = await prisma.rental.update({
    where: { id: rentalId },
    data: { returnedAt: new Date() },
  });

  await prisma.book.update({ where: { id: rental.bookId }, data: { isRented: false } });
  res.json(rental);
};
