#!/bin/bash

echo "🚀 SARVA MICROSERVICES DEMO"
echo "=========================================="
echo ""

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

AUTH_URL="http://localhost:8001"
WALLET_URL="http://localhost:8002"

TIMESTAMP=$(date +%s)
TEST_EMAIL="demo${TIMESTAMP}@sarva.com"
TEST_PASSWORD="DemoPass123!"

echo -e "${CYAN}PART 1: AUTHENTICATION SERVICE${NC}"
echo ""

echo -e "${BLUE}[1.1] Health Check - Auth Service${NC}"
curl -s $AUTH_URL/health | jq .
echo ""
sleep 1

echo -e "${BLUE}[1.2] Register New User${NC}"
echo "Email: $TEST_EMAIL"
REGISTER_RESPONSE=$(curl -s -X POST $AUTH_URL/api/auth/register -H "Content-Type: application/json" -d "{\"email\":\"$TEST_EMAIL\",\"password\":\"$TEST_PASSWORD\",\"firstName\":\"Demo\",\"lastName\":\"User\"}")
echo "$REGISTER_RESPONSE" | jq .
echo ""
sleep 1

USER_ID=$(echo "$REGISTER_RESPONSE" | jq -r '.user.id')
echo -e "${GREEN}User ID: $USER_ID${NC}"
echo ""
sleep 1

echo -e "${BLUE}[1.3] Login User${NC}"
LOGIN_RESPONSE=$(curl -s -X POST $AUTH_URL/api/auth/login -H "Content-Type: application/json" -d "{\"email\":\"$TEST_EMAIL\",\"password\":\"$TEST_PASSWORD\"}")
echo "$LOGIN_RESPONSE" | jq .
echo ""

TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.token')
echo -e "${GREEN}Token received${NC}"
echo ""
sleep 1

echo ""
echo -e "${CYAN}PART 2: WALLET SERVICE${NC}"
echo ""

echo -e "${BLUE}[2.1] Health Check - Wallet Service${NC}"
curl -s $WALLET_URL/health | jq .
echo ""
sleep 1

echo -e "${BLUE}[2.2] Get Wallet${NC}"
curl -s -X GET $WALLET_URL/api/wallet -H "Authorization: Bearer $TOKEN" | jq .
echo ""
sleep 1

echo -e "${BLUE}[2.3] Deposit \$1,000${NC}"
curl -s -X POST $WALLET_URL/api/wallet/deposit -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"amount":1000,"description":"Initial funding"}' | jq .
echo ""
sleep 1

echo -e "${BLUE}[2.4] Deposit \$500${NC}"
curl -s -X POST $WALLET_URL/api/wallet/deposit -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"amount":500,"description":"Additional funds"}' | jq .
echo ""
sleep 1

echo -e "${BLUE}[2.5] Withdraw \$300${NC}"
curl -s -X POST $WALLET_URL/api/wallet/withdraw -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"amount":300,"description":"Purchase"}' | jq .
echo ""
sleep 1

echo -e "${BLUE}[2.6] Transaction History${NC}"
curl -s -X GET $WALLET_URL/api/wallet/transactions -H "Authorization: Bearer $TOKEN" | jq .
echo ""
sleep 1

echo -e "${BLUE}[2.7] Final Balance${NC}"
FINAL_WALLET=$(curl -s -X GET $WALLET_URL/api/wallet -H "Authorization: Bearer $TOKEN")
echo "$FINAL_WALLET" | jq .
FINAL_BALANCE=$(echo "$FINAL_WALLET" | jq -r '.wallet.balance')
echo ""

echo ""
echo -e "${GREEN}🎉 DEMO COMPLETE${NC}"
echo "User: $TEST_EMAIL"
echo "Final Balance: \$$FINAL_BALANCE"
echo ""
