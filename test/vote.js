const { ethers } = require("hardhat");

async function main() {
  const contractAddress = "0x22Af5f2b7755736Fb35260429592231ff387Da1C"; // <- Replace with your deployed contract address

  const poll = await ethers.getContractAt("Poll", contractAddress);
  const [voter] = await ethers.getSigners();

  console.log("Connected as:", voter.address);

  // 👉 Read poll question and options
  const question = await poll.question();
  const options = await Promise.all([
    poll.options(0),
    poll.options(1),
    poll.options(2),
    poll.options(3)
  ]);

  console.log("\n📋 Poll Question:", question);
  options.forEach((opt, i) => console.log(`${i}: ${opt}`));

  // 👉 Vote for an option (e.g., index 2 = "Solidity")
  const selectedOption = 1;
  console.log(`\n🗳️ Voting for option ${selectedOption}: "${options[selectedOption]}"`);
  const tx = await poll.connect(voter).vote(selectedOption);
  await tx.wait();
  console.log("✅ Vote submitted.");

  // 👉 Fetch and display results
  const votes = await poll.getVotes();
  console.log("\n📊 Current Vote Counts:");
  votes.forEach((v, i) => {
    console.log(`${options[i]}: ${v.toString()} votes`);
  });

  // 👉 Get current leading option
  const [leadingOption, voteCount] = await poll.getLeadingOption();
  console.log(`\n🏆 Leading Option: ${leadingOption} (${voteCount.toString()} votes)`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
