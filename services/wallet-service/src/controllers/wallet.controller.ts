import { Request, Response } from 'express';
import { WalletService } from '../services/wallet.service';

const walletService = new WalletService();

export class WalletController {
  async getWallet(req: Request, res: Response) {
    try {
      const userId = (req as any).userId;
      const wallet = await walletService.getOrCreateWallet(userId);
      
      res.json({
        wallet: {
          id: wallet.id,
          balance: wallet.balance.toString(),
          currency: wallet.currency,
        },
      });
    } catch (error: any) {
      console.error('Get wallet error:', error);
      res.status(500).json({ error: 'Failed to get wallet' });
    }
  }

  async deposit(req: Request, res: Response) {
    try {
      const userId = (req as any).userId;
      const { amount, description } = req.body;

      if (!amount || amount <= 0) {
        return res.status(400).json({ error: 'Invalid amount' });
      }

      const result = await walletService.deposit(userId, parseFloat(amount), description);

      res.json({
        message: 'Deposit successful',
        wallet: { balance: result.wallet.balance.toString() },
        transaction: {
          id: result.transaction.id,
          amount: result.transaction.amount.toString(),
        },
      });
    } catch (error: any) {
      res.status(500).json({ error: 'Deposit failed' });
    }
  }

  async withdraw(req: Request, res: Response) {
    try {
      const userId = (req as any).userId;
      const { amount, description } = req.body;

      if (!amount || amount <= 0) {
        return res.status(400).json({ error: 'Invalid amount' });
      }

      const result = await walletService.withdraw(userId, parseFloat(amount), description);

      res.json({
        message: 'Withdrawal successful',
        wallet: { balance: result.wallet.balance.toString() },
      });
    } catch (error: any) {
      const message = error.message === 'Insufficient balance' ? error.message : 'Withdrawal failed';
      res.status(error.message === 'Insufficient balance' ? 400 : 500).json({ error: message });
    }
  }

  async getTransactions(req: Request, res: Response) {
    try {
      const userId = (req as any).userId;
      const transactions = await walletService.getTransactions(userId);

      res.json({
        transactions: transactions.map(tx => ({
          id: tx.id,
          type: tx.type,
          amount: tx.amount.toString(),
          description: tx.description,
          createdAt: tx.createdAt,
        })),
      });
    } catch (error: any) {
      res.status(500).json({ error: 'Failed to get transactions' });
    }
  }
}
