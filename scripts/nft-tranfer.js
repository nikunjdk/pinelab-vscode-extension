const { ethers } = require("hardhat");

async function main() {
  const contractAddress = "0xE4A80b8529Be90ca8D889fb66fAc033322733bd7";
  const tokenId = 2; // Replace with the actual token ID you want to transfer
  const recipientAddress = ""; // Replace with the actual recipient address

  const [sender] = await ethers.getSigners(); // current NFT owner

  const nft = await ethers.getContractAt("InfNFT", contractAddress, sender);

  const tx = await nft["safeTransferFrom(address,address,uint256)"](
    sender.address,
    recipientAddress,
    tokenId
  );
  await tx.wait();

  console.log(`NFT ID ${tokenId} transferred from ${sender.address} to ${recipientAddress}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
