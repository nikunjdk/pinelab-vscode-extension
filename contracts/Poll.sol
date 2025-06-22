// SPDX-License-Identifier: MIT
// Compatible with OpenZeppelin Contracts ^5.0.0
pragma solidity ^0.8.27;

contract Poll {
    string public question;
    string[4] public options;
    uint256[4] public votes;

    mapping(address => bool) public hasVoted;

    constructor(string memory _question, string[4] memory _options) {
        question = _question;
        options = _options;
    }

    function vote(uint8 optionIndex) external {
        require(optionIndex < 4, "Invalid option");
        require(!hasVoted[msg.sender], "You have already voted");

        votes[optionIndex]++;
        hasVoted[msg.sender] = true;
    }

    function getVotes() external view returns (uint256[4] memory) {
        return votes;
    }

    function getLeadingOption() external view returns (string memory option, uint256 voteCount) {
        uint256 maxVotes = votes[0];
        uint8 leadingIndex = 0;

        for (uint8 i = 1; i < 4; i++) {
            if (votes[i] > maxVotes) {
                maxVotes = votes[i];
                leadingIndex = i;
            }
        }

        return (options[leadingIndex], maxVotes);
    }
}
