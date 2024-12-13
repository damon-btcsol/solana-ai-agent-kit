# src/solana_agentkit/agent/solana_agent.py

from typing import Optional, Dict, Any, Union, List
from dataclasses import dataclass
from rsa import PublicKey
from solana.rpc.api import Client
import base58
from langchain.llms import BaseLLM
from langchain.agents import Tool
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
#from solana.publickey import PublicKey
from solana_agentkit.utils import keypair
from .base import BaseAgent
#from solders.pubkey import Pubkey as PublicKey
@dataclass
class CollectionOptions:
    """Options for deploying an NFT collection."""
    name: str
    symbol: str
    description: str
    image_url: str
    seller_fee_basis_points: int = 0

@dataclass
class PumpFunTokenOptions:
    """Options for launching a PumpFun token."""
    max_supply: Optional[int] = None
    initial_price: Optional[float] = None
    liquidity_percentage: Optional[float] = None

class SolanaAgent(BaseAgent):
    """
    AI-powered agent for interacting with the Solana blockchain.
    Combines LangChain capabilities with Solana operations.
    """
    
    def __init__(
        self,
        private_key: str,
        llm: BaseLLM,
        rpc_url: str = "https://api.mainnet-beta.solana.com",
        openai_api_key: Optional[str] = None
    ):
        """
        Initialize Solana Agent.
        
        Args:
            private_key: Base58 encoded private key
            llm: Language model for agent reasoning
            rpc_url: Solana RPC endpoint URL
            openai_api_key: OpenAI API key for AI features
        """
        super().__init__(keypair=keypair.from_secret_key(base58.b58decode(private_key)), rpc_url=rpc_url)
        self.wallet_address = self.keypair.public_key
        self.openai_api_key = openai_api_key
        
        # AI setup
        self.llm = llm
        self.tools = self._initialize_tools()
        self.agent_chain = self._create_agent_chain()

    def _initialize_tools(self) -> List[Tool]:
        """Initialize available tools for the agent."""
        return [
            Tool(
                name="deploy_token",
                func=self.deploy_token,
                description="Deploy a new SPL token with specified decimals"
            ),
            Tool(
                name="deploy_collection",
                func=self.deploy_collection,
                description="Deploy a new NFT collection with specified options"
            ),
            Tool(
                name="get_balance",
                func=self.get_balance,
                description="Get wallet balance for SOL or SPL token"
            ),
            # Add other tools here
        ]

    def _create_agent_chain(self) -> LLMChain:
        """Create the main agent reasoning chain."""
        template = """You are a Solana blockchain agent with the following capabilities:
        - Deploy tokens and NFT collections
        - Execute trades and transfers
        - Manage domains and other blockchain operations
        
        User request: {input}
        
        Think through the steps needed and use available tools to fulfill this request.
        
        Available tools: {tools}
        
        Response:"""
        
        prompt = PromptTemplate(
            input_variables=["input", "tools"],
            template=template
        )
        
        return LLMChain(
            llm=self.llm,
            prompt=prompt
        )

    async def process_message(self, message: str) -> str:
        """
        Process a user message and execute requested operations.
        
        Args:
            message: User input message
            
        Returns:
            Agent response and action results
        """
        # Use LLM to understand intent
        response = await self.agent_chain.arun(
            input=message,
            tools=", ".join(tool.name for tool in self.tools)
        )
        
        # Execute determined actions
        # This is a simplified implementation - you might want to add
        # more sophisticated action parsing and execution logic
        return response

    # Blockchain operation methods
    async def deploy_token(
        self,
        decimals: int = 9
    ) -> Dict[str, Any]:
        """Deploy a new SPL token."""
        from ..tools import deploy_token
        return await deploy_token(self, decimals)

    async def deploy_collection(
        self,
        options: CollectionOptions
    ) -> Dict[str, Any]:
        """Deploy an NFT collection."""
        from ..tools import deploy_collection
        return await deploy_collection(self, options)

    async def get_balance(
        self,
        token_address: Optional[PublicKey] = None
    ) -> Union[int, float]:
        """Get wallet balance."""
        from ..tools import get_balance
        return await get_balance(self, token_address)

    async def mint_nft(
        self,
        collection_mint: PublicKey,
        metadata: Dict[str, Any],
        recipient: Optional[PublicKey] = None
    ) -> Dict[str, Any]:
        """Mint an NFT from a collection."""
        from ..tools import mint_collection_nft
        return await mint_collection_nft(self, collection_mint, metadata, recipient)

    async def transfer(
        self,
        to: PublicKey,
        amount: float,
        mint: Optional[PublicKey] = None
    ) -> Dict[str, Any]:
        """Transfer SOL or tokens."""
        from ..tools import transfer
        return await transfer(self, to, amount, mint)

    async def trade(
        self,
        output_mint: PublicKey,
        input_amount: float,
        input_mint: Optional[PublicKey] = None,
        slippage_bps: int = 50
    ) -> Dict[str, Any]:
        """Execute a token swap."""
        from ..tools import trade
        return await trade(self, output_mint, input_amount, input_mint, slippage_bps)

    async def launch_pumpfun_token(
        self,
        token_name: str,
        token_ticker: str,
        description: str,
        image_url: str,
        options: Optional[PumpFunTokenOptions] = None
    ) -> Dict[str, Any]:
        """Launch a PumpFun token."""
        from ..tools import launch_pumpfun_token
        return await launch_pumpfun_token(
            self,
            token_name,
            token_ticker,
            description,
            image_url,
            options
        )