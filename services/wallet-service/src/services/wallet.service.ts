import { PrismaClient, TransactionType } from '@prisma/client';

const prisma = new PrismaClient();

export class WalletService {
  async getOrCreateWallet(userId: string) {
    let wallet = await prisma.wallet.findUnique({
      where: { userId },
    });

    if (!wallet) {
      wallet = await prisma.wallet.create({
        data: {
          userId,
          balance: 0,
          currency: 'USD',
        },
      });
    }

    return wallet;
  }

  async deposit(userId: string, amount: number, description?: string) {
    const wallet = await this.getOrCreateWallet(userId);

    const result = await prisma.$transaction(async (tx) => {
      const updatedWallet = await tx.wallet.update({
        where: { id: wallet.id },
        data: { balance: { increment: amount } },
      });

      const transaction = await tx.transaction.create({
        data: {
          walletId: wallet.id,
          type: TransactionType.DEPOSIT,
          amount,
          balanceBefore: wallet.balance,
          balanceAfter: updatedWallet.balance,
          description: description || 'Deposit',
          status: 'completed',
        },
      });

      return { wallet: updatedWallet, transaction };
    });

    return result;
  }

  async withdraw(userId: string, amount: number, description?: string) {
    const wallet = await this.getOrCreateWallet(userId);

    if (wallet.balance < amount) {
      throw new Error('Insufficient balance');
    }

    const result = await prisma.$transaction(async (tx) => {
      const updatedWallet = await tx.wallet.update({
        where: { id: wallet.id },
        data: { balance: { decrement: amount } },
      });

      const transaction = await tx.transaction.create({
        data: {
          walletId: wallet.id,
          type: TransactionType.WITHDRAWAL,
          amount,
          balanceBefore: wallet.balance,
          balanceAfter: updatedWallet.balance,
          description: description || 'Withdrawal',
          status: 'completed',
        },
      });

      return { wallet: updatedWallet, transaction };
    });

    return result;
  }

  async getTransactions(userId: string, limit: number = 50) {
    const wallet = await this.getOrCreateWallet(userId);

    const transactions = await prisma.transaction.findMany({
      where: { walletId: wallet.id },
      orderBy: { createdAt: 'desc' },
      take: limit,
    });

    return transactions;
  }
}
