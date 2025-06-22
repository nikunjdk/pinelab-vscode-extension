const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();

  console.log("Deploying InfNFT contract with account:", deployer.address);

  const InfNFT = await hre.ethers.getContractFactory("InfNFT");
  const infNFT = await InfNFT.deploy(deployer.address);

  await infNFT.deployed();
  console.log("InfNFT contract deployed to:", infNFT.address);

  // Mint a test NFT
  const metadataURI = ""; // replace with real metadata URI
  const tx = await infNFT.safeMint(deployer.address, metadataURI);
  const receipt = await tx.wait();

  console.log(`Minted NFT to ${deployer.address}`);
  console.log(`Transaction hash: ${receipt.transactionHash}`);
}

// Use async/await and proper error handling
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
