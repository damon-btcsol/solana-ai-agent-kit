# src/solana_agentkit/constants.py


from typing import Dict, Final
from dataclasses import dataclass

from rsa import PublicKey

class TokenAddresses:
    """
    Common token addresses used across the toolkit.
    
    These addresses represent the official mint addresses for various tokens
    on the Solana blockchain. They are used for token identification and
    interaction throughout the application.
    """
    
    USDC: Final[PublicKey] = PublicKey("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")
    USDT: Final[PublicKey] = PublicKey("Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB")
    USDS: Final[PublicKey] = PublicKey("USDSwr9ApdHk5bvJKMjzff41FfuX8bSxdKcR81vTwcA")
    SOL: Final[PublicKey] = PublicKey("So11111111111111111111111111111111111111112")
    JITO_SOL: Final[PublicKey] = PublicKey("J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn")
    B_SOL: Final[PublicKey] = PublicKey("bSo13r4TkiE4KumL71LsHTPpL2euBYLFx6h9HP3piy1")
    M_SOL: Final[PublicKey] = PublicKey("mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So")
    BONK: Final[PublicKey] = PublicKey("DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263")

@dataclass(frozen=True)
class DefaultOptions:
    """
    Default configuration options for the toolkit.
    
    Attributes:
        SLIPPAGE_BPS: Default slippage tolerance in basis points (300 = 3%)
        TOKEN_DECIMALS: Default number of decimals for new tokens
    """
    
    SLIPPAGE_BPS: int = 300
    TOKEN_DECIMALS: int = 9

class APIEndpoints:
    """
    API endpoints used by the toolkit.
    
    These endpoints are used for various service integrations including
    Jupiter for trading and LULO (formerly Flexlend) for lending operations.
    """
    
    JUPITER: Final[str] = "https://quote-api.jup.ag/v6"
    LULO: Final[str] = "https://api.flexlend.fi"

# Create singleton instances
TOKENS = TokenAddresses()
OPTIONS = DefaultOptions()
APIS = APIEndpoints()

# Type hints for better IDE support
TokenDict = Dict[str, PublicKey]

def get_token_by_symbol(symbol: str) -> PublicKey:
    """
    Get a token's PublicKey by its symbol.
    
    Args:
        symbol: Token symbol (e.g., 'USDC', 'SOL')
        
    Returns:
        PublicKey for the specified token
        
    Raises:
        AttributeError: If token symbol is not found
    """
    return getattr(TOKENS, symbol)

# Example usage:
# from solana_agentkit.constants import TOKENS, OPTIONS, APIS
# 
# usdc_address = TOKENS.USDC
# default_slippage = OPTIONS.SLIPPAGE_BPS
# jupiter_api = APIS.JUPITER