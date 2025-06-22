const { ethers } = require("hardhat");

async function main() {
  const contractAddress = "0xE4A80b8529Be90ca8D889fb66fAc033322733bd7";
  const metadataURI = "";

  const [owner] = await ethers.getSigners();

  const nft = await ethers.getContractAt("InfNFT", contractAddress, owner);
  const tx = await nft.safeMint(owner.address, metadataURI);
  await tx.wait();

  console.log("NFT minted to:", owner.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
