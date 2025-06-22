const { ethers } = require("hardhat");
const axios = require("axios");

const IPFS_GATEWAY = "https://gateway.pinata.cloud/ipfs/";

async function main() {
  const contractAddress = "0xE4A80b8529Be90ca8D889fb66fAc033322733bd7";
  const [wallet] = await ethers.getSigners();

  const nft = await ethers.getContractAt("InfNFT", contractAddress, wallet);
  const balance = await nft.balanceOf(wallet.address);
  console.log(`🧾 NFT Balance: ${balance}`);

  for (let i = 0; i < balance; i++) {
    const tokenId = await nft.tokenOfOwnerByIndex(wallet.address, i);
    const uri = await nft.tokenURI(tokenId);

    console.log(`\n📦 Token #${tokenId}:`);
    console.log(`URI: ${uri}`);

    try {
      // Replace ipfs:// with HTTPS gateway
      const ipfsUrl = uri.replace("ipfs://", IPFS_GATEWAY);
      const res = await axios.get(ipfsUrl);
      console.log("🖼️ Name:", res.data.name);
      console.log("📄 Description:", res.data.description);
      console.log("🖼️ Image URL:", res.data.image.replace("ipfs://", IPFS_GATEWAY));
    } catch (err) {
      console.log("⚠️ Failed to fetch metadata:", err.message);
    }
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
