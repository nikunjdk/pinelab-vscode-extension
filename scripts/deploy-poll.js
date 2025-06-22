const { ethers } = require("hardhat");

async function main() {
  const Poll = await ethers.getContractFactory("Poll");

  const question = "What is your favorite programming language?";
  const options = [
    "JavaScript",
    "Python",
    "Solidity",
    "Rust"
  ];

  const poll = await Poll.deploy(question, options);
  await poll.deployed();

  console.log("Poll deployed to:", poll.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
